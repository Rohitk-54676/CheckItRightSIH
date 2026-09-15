
"use client";

import Link from "next/link";
import { FileText, MapPin } from "lucide-react";

const reviewData = [
  {
    id: "1",
    code: "RPT-2026-001",
    productName: "Packaged Drinking Water",
    issueType: "Net Quantity",
    locationText: "Kohima, Nagaland",
    createdAt: "15 Sep 2026, 10:30 AM",
  },
  {
    id: "2",
    code: "RPT-2026-002",
    productName: "Instant Noodles",
    issueType: "MRP",
    locationText: "Dimapur, Nagaland",
    createdAt: "15 Sep 2026, 09:15 AM",
  },
  {
    id: "3",
    code: "RPT-2026-003",
    productName: "Cooking Oil",
    issueType: "Expiry Date",
    locationText: "Imphal, Manipur",
    createdAt: "14 Sep 2026, 04:45 PM",
  },
  {
    id: "4",
    code: "RPT-2026-004",
    productName: "Packaged Rice",
    issueType: "Product Name",
    locationText: "Aizawl, Mizoram",
    createdAt: "14 Sep 2026, 02:20 PM",
  },
];

export default function ReviewQueue() {
  return (
    <div className="rounded-xl border border-[#D9E2EC] bg-white shadow-sm">
      <div className="flex items-center justify-between border-b border-[#D9E2EC] px-5 py-4">
        <h3 className="text-sm font-bold text-[#102A43]">
          Pending Review
          <span className="ml-2 rounded-full bg-[#FFF6DF] px-2 py-0.5 text-[10px] font-semibold text-[#B45309]">
            {reviewData.length}
          </span>
        </h3>

        <Link
          href="/reviewer/reports"
          className="text-xs font-semibold text-[#1769AA] hover:underline"
        >
          View all →
        </Link>
      </div>

      <div className="divide-y divide-[#EAF0F6]">
        {reviewData.map((report) => (
          <Link
            key={report.id}
            href={`/reviewer/reports/${report.id}`}
            className="block px-5 py-4 transition hover:bg-[#F7FAFC]"
          >
            <div className="flex items-start justify-between gap-3">
              <div className="flex min-w-0 gap-3">
                <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-[#EFF6FF]">
                  <FileText className="h-4 w-4 text-[#1769AA]" />
                </div>

                <div className="min-w-0">
                  <p className="text-xs font-mono text-[#829AB1]">
                    {report.code}
                  </p>

                  <p className="mt-0.5 truncate text-sm font-semibold text-[#102A43]">
                    {report.productName}
                  </p>

                  <div className="mt-1 flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-[#627D98]">
                    <span className="rounded bg-[#FEECEC] px-1.5 py-0.5 text-[10px] font-semibold text-[#DC2626]">
                      {report.issueType}
                    </span>

                    <span className="inline-flex items-center gap-1">
                      <MapPin className="h-3 w-3" />
                      {report.locationText}
                    </span>
                  </div>

                  <p className="mt-1.5 text-[11px] text-[#829AB1]">
                    {report.createdAt}
                  </p>
                </div>
              </div>

              <span className="shrink-0 rounded-full bg-[#FEF3C7] px-2.5 py-1 text-[10px] font-semibold text-[#B45309]">
                Pending
              </span>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}

