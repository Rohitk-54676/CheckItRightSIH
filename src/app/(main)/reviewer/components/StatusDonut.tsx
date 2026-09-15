
"use client";

const segments = [
  {
    key: "pending",
    label: "Pending",
    value: 12,
    color: "#F59E0B",
  },
  {
    key: "forwarded",
    label: "Forwarded",
    value: 28,
    color: "#1769AA",
  },
  {
    key: "rejected",
    label: "Rejected",
    value: 8,
    color: "#DC2626",
  },
  {
    key: "resolved",
    label: "Resolved",
    value: 18,
    color: "#16A34A",
  },
];

export default function StatusDonut() {
  const size = 160;
  const stroke = 18;
  const r = (size - stroke) / 2;
  const circ = 2 * Math.PI * r;

  const total = segments.reduce((sum, segment) => {
    return sum + segment.value;
  }, 0);

  const arcs = segments.map((segment, index) => {
    const dash = (segment.value / total) * circ;
    const offset = segments
      .slice(0, index)
      .reduce((sum, previousSegment) => {
        return sum + (previousSegment.value / total) * circ;
      }, 0);

    return {
      ...segment,
      dash,
      offset,
    };
  });

  return (
    <div className="rounded-xl border border-[#D9E2EC] bg-white p-5 shadow-sm">
      <h3 className="text-sm font-bold text-[#102A43]">
        Reports by Status
      </h3>

      <div className="mt-5 flex flex-col items-center gap-6 sm:flex-row">
        {/* Donut Chart */}
        <div className="relative shrink-0">
          <svg width={size} height={size} className="-rotate-90">
            {/* Background Circle */}
            <circle
              cx={size / 2}
              cy={size / 2}
              r={r}
              fill="none"
              stroke="#EAF4FF"
              strokeWidth={stroke}
            />

            {/* Status Arcs */}
            {arcs.map((arc) => (
              <circle
                key={arc.key}
                cx={size / 2}
                cy={size / 2}
                r={r}
                fill="none"
                stroke={arc.color}
                strokeWidth={stroke}
                strokeDasharray={`${arc.dash} ${circ - arc.dash}`}
                strokeDashoffset={-arc.offset}
              />
            ))}
          </svg>

          {/* Center Text */}
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className="text-2xl font-bold text-[#102A43]">
              {total}
            </span>

            <span className="text-[10px] font-medium uppercase tracking-wider text-[#627D98]">
              Reports
            </span>
          </div>
        </div>

        {/* Legend */}
        <ul className="flex w-full flex-col gap-2.5">
          {segments.map((segment) => (
            <li
              key={segment.key}
              className="flex items-center gap-2 text-xs"
            >
              <span
                className="h-2.5 w-2.5 shrink-0 rounded-full"
                style={{ background: segment.color }}
              />

              <span className="flex-1 text-[#102A43]">
                {segment.label}
              </span>

              <span className="font-semibold text-[#102A43]">
                {segment.value}
              </span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

