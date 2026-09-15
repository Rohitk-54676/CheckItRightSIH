
"use client";

import {
  Scale,
  Tag,
  CalendarX,
  IndianRupee,
  HelpCircle,
} from "lucide-react";

const issueData = [
  {
    label: "Net Quantity",
    value: 18,
    color: "#3B82F6",
    icon: Scale,
  },
  {
    label: "Product Name",
    value: 14,
    color: "#10B981",
    icon: Tag,
  },
  {
    label: "Expiry Date",
    value: 10,
    color: "#F59E0B",
    icon: CalendarX,
  },
  {
    label: "MRP",
    value: 8,
    color: "#EF4444",
    icon: IndianRupee,
  },
  {
    label: "Other",
    value: 5,
    color: "#8B5CF6",
    icon: HelpCircle,
  },
];

export default function IssueTypeChart() {
  const max = Math.max(...issueData.map((d) => d.value));

  return (
    <div className="rounded-xl border border-[#D9E2EC] bg-white p-5 shadow-sm">
      <h3 className="text-sm font-bold text-[#102A43]">
        Reports by Issue Type
      </h3>

      <div className="mt-5 space-y-3">
        {issueData.map((item) => {
          const Icon = item.icon;
          const pct = Math.round((item.value / max) * 100);

          return (
            <div key={item.label} className="flex items-center gap-3">
              <Icon className="h-3.5 w-3.5 shrink-0 text-[#627D98]" />

              <span className="w-32 shrink-0 truncate text-[11px] font-medium text-[#102A43]">
                {item.label}
              </span>

              <div className="relative h-2 flex-1 overflow-hidden rounded-full bg-[#EAF4FF]">
                <div
                  className="h-full rounded-full"
                  style={{
                    width: `${pct}%`,
                    background: item.color,
                  }}
                />
              </div>

              <span className="w-6 shrink-0 text-right text-[11px] font-bold text-[#102A43]">
                {item.value}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}

