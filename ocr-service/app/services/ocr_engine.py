import os

os.environ["FLAGS_use_onednn"] = "0"
os.environ["FLAGS_enable_pir_api"] = "0"

import cv2
import numpy as np

from paddleocr import PaddleOCR


def _resolve_device(requested_device: str) -> str:
    """
    If "gpu" is requested but not actually usable (paddlepaddle-gpu not
    installed, no CUDA device visible, driver mismatch, etc), fall back
    to "cpu" ourselves and say so clearly.

    This matters because letting Paddle discover "GPU not available"
    internally and silently switch to CPU mid-flight skips OUR
    enable_mkldnn=False setting for the CPU path, which is what
    triggers the oneDNN/PIR crash we've hit before. Deciding the
    device up front avoids that entirely.
    """
    if requested_device != "gpu":
        return requested_device

    try:
        import paddle

        if (
            paddle.device.is_compiled_with_cuda()
            and paddle.device.cuda.device_count() > 0
        ):
            return "gpu"

        print(
            "OCR ENGINE: OCR_DEVICE=gpu was requested, but this "
            "paddlepaddle install has no usable CUDA GPU "
            "(paddlepaddle-gpu not installed, or no GPU detected). "
            "Falling back to CPU."
        )
    except Exception as error:
        print(
            "OCR ENGINE: GPU availability check failed "
            f"({error!r}); falling back to CPU."
        )

    return "cpu"


class OCREngine:
    def __init__(
        self,
        lang: str = "en",
        device: str = "cpu",
        cpu_threads: int = 4,
    ):
        device = _resolve_device(device)

        # ------------------------------------------------------------
        # PaddleOCR 3.x by default runs THREE extra models on top of
        # detection+recognition: doc-orientation-classify, doc-unwarping,
        # and textline-orientation. These are unnecessary for normal,
        # upright phone/scan photos, so we turn them off.
        #
        # We also pin the "mobile" (lightweight) detection + recognition
        # models instead of the default "server" models — much faster,
        # on both CPU and GPU.
        #
        # The bottleneck on label images was recognition running one
        # text box at a time (product labels can have 150-200+ small
        # text detections). text_recognition_batch_size lets multiple
        # crops be recognized in one batched forward pass instead of
        # one-by-one.
        #
        # enable_mkldnn stays OFF on CPU: on this Paddle build, mkldnn +
        # the PIR executor crashes on certain ops.
        #
        # cpu_threads is only relevant when device="cpu" and is kept
        # modest (not "all cores") — testing showed handing a single
        # inference call a very large thread count (e.g. 14) makes it
        # SLOWER, not faster, because these are lots of small ops and
        # thread coordination overhead dominates. On GPU this setting
        # is simply ignored by Paddle.
        # ------------------------------------------------------------
        candidate_kwargs = {
            "lang": lang,
            "device": device,
            "enable_mkldnn": False,
            "cpu_threads": cpu_threads,
            "use_doc_orientation_classify": False,
            "use_doc_unwarping": False,
            "use_textline_orientation": False,
            "text_detection_model_name": "PP-OCRv5_mobile_det",
            "text_recognition_model_name": "PP-OCRv5_mobile_rec",
            "text_det_limit_side_len": 960,
            "text_recognition_batch_size": 32,
        }

        try:
            self.ocr = PaddleOCR(**candidate_kwargs)
        except (TypeError, ValueError) as error:
            # Some param name isn't supported by this paddleocr/paddlex
            # version — fall back to only the parameters we're confident
            # about rather than crashing the whole service.
            print(
                "OCR ENGINE: full kwargs failed "
                f"({error!r}), retrying with a "
                "reduced, safer parameter set"
            )

            safe_kwargs = {
                "device": device,
                "enable_mkldnn": False,
                "cpu_threads": cpu_threads,
                "use_doc_orientation_classify": False,
                "use_doc_unwarping": False,
                "use_textline_orientation": False,
                "text_detection_model_name": "PP-OCRv5_mobile_det",
                "text_recognition_model_name": "PP-OCRv5_mobile_rec",
            }

            try:
                self.ocr = PaddleOCR(**safe_kwargs)
            except (TypeError, ValueError) as error2:
                print(
                    "OCR ENGINE: reduced kwargs also failed "
                    f"({error2!r}), falling back to the "
                    "original minimal config"
                )

                self.ocr = PaddleOCR(
                    lang=lang,
                    device=device,
                    enable_mkldnn=False,
                )

    def process_image(
        self,
        image: np.ndarray,
    ) -> dict:

        # --------------------------------
        # Convert grayscale to BGR
        # --------------------------------

        if len(image.shape) == 2:
            image_for_ocr = cv2.cvtColor(
                image,
                cv2.COLOR_GRAY2BGR,
            )
        else:
            image_for_ocr = image

        # --------------------------------
        # Run PaddleOCR directly on the in-memory array.
        # PaddleOCR.predict() accepts a numpy array (BGR) natively,
        # so the previous encode -> write-to-disk -> re-read-from-disk
        # round trip was pure overhead. Removing it saves disk I/O
        # and a PNG encode/decode per image.
        # --------------------------------

        result = self.ocr.predict(
            image_for_ocr
        )

        # --------------------------------
        # Parse OCR result
        # --------------------------------

        detections = []

        for page in result:

            texts = page.get(
                "rec_texts",
                [],
            )

            scores = page.get(
                "rec_scores",
                [],
            )

            boxes = page.get(
                "rec_boxes",
                [],
            )

            for text, score, box in zip(
                texts,
                scores,
                boxes,
            ):
                detections.append(
                    {
                        "text": str(text),
                        "confidence": round(
                            float(score),
                            4,
                        ),
                        "bbox": box.tolist(),
                    }
                )

        # --------------------------------
        # Average confidence
        # --------------------------------

        average_confidence = 0.0

        if detections:
            average_confidence = round(
                sum(
                    item["confidence"]
                    for item in detections
                )
                / len(detections),
                4,
            )

        # --------------------------------
        # Final OCR result
        # --------------------------------

        return {
            "text": "\n".join(
                item["text"]
                for item in detections
            ),
            "detections": detections,
            "average_confidence": (
                average_confidence
            ),
            "detection_count": len(
                detections
            ),
            "engine": "PaddleOCR",
            "language": "en",
        }


class OCREnginePool:
    """
    A small pool of independent OCREngine instances so multiple images
    can run through PaddleOCR truly in parallel.

    A single PaddleOCR predictor is NOT safe to call concurrently from
    multiple threads at once — so instead of sharing one instance across
    threads (which risks corrupted/incorrect results or crashes), we
    keep a few fully independent instances and hand each worker thread
    its own instance from a queue.
    """

    def __init__(
        self,
        size: int = 2,
        cpu_threads_per_engine: int = 4,
        device: str = "cpu",
    ):
        import queue

        self._queue: "queue.Queue[OCREngine]" = queue.Queue()

        for _ in range(size):
            self._queue.put(
                OCREngine(
                    device=device,
                    cpu_threads=cpu_threads_per_engine,
                )
            )

    def process_image(self, image: np.ndarray) -> dict:
        engine = self._queue.get()

        try:
            return engine.process_image(image)
        finally:
            self._queue.put(engine)


import os as _os

# ------------------------------------------------------------------
# Device selection: set the OCR_DEVICE environment variable to "gpu"
# to run on an NVIDIA GPU (requires paddlepaddle-gpu installed, matching
# your CUDA version — see: https://www.paddlepaddle.org.cn/en/install/quick).
# Defaults to "cpu" so the service still works out of the box without
# a GPU / without paddlepaddle-gpu installed.
#
# GPU vs CPU changes concurrency strategy too:
#   - GPU: a single engine, calls are serialized (queue of size 1).
#     One CUDA context is far simpler/safer to share this way, and a
#     single GPU call over the whole 150-200 detections image is
#     already much faster than any CPU config we tried — no need for
#     the multi-engine juggling.
#   - CPU: keep 2 engines, but with a MODEST thread count each. Testing
#     showed handing one inference call a very large thread count (e.g.
#     14 threads on a 28-thread CPU) made it slower, not faster — lots
#     of small per-text-box ops don't parallelize well past a point.
# ------------------------------------------------------------------
OCR_DEVICE = _os.environ.get("OCR_DEVICE", "cpu").strip().lower()

if OCR_DEVICE == "gpu":
    _POOL_SIZE = 1
    _THREADS_PER_ENGINE = 4  # ignored by Paddle on GPU, harmless
else:
    _TOTAL_CORES = _os.cpu_count() or 4
    _POOL_SIZE = 2 if _TOTAL_CORES >= 4 else 1
    _THREADS_PER_ENGINE = min(6, max(1, _TOTAL_CORES // _POOL_SIZE))

# Public so app/api/ocr.py can cap its own concurrency to match the
# number of engines actually available — no point spinning up more
# concurrent image pipelines than we have engines to serve them,
# since the extra ones just sit there burning CPU on preprocessing
# while waiting for an engine anyway.
OCR_POOL_SIZE = _POOL_SIZE

ocr_engine = OCREnginePool(
    size=_POOL_SIZE,
    cpu_threads_per_engine=_THREADS_PER_ENGINE,
    device=OCR_DEVICE,
)