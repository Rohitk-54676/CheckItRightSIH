
"use client";

import { FileText, Forward, CheckCircle2 } from "lucide-react";

const CARDS = [
  {
    label: "Pending Reviews",
    value: 12,
    hint: "Awaiting your decision",
    icon: FileText,
    bg: "bg-[#FFF6DF]",
    color: "text-[#F59E0B]",
  },
  {
    label: "Forwarded Cases",
    value: 28,
    hint: "Sent to inspector pool",
    icon: Forward,
    bg: "bg-[#E8F1FB]",
    color: "text-[#1769AA]",
  },
  {
    label: "Reviewed by You",
    value: 46,
    hint: "Forwarded or rejected",
    icon: CheckCircle2,
    bg: "bg-[#EAF8F0]",
    color: "text-[#16A34A]",
  },
];

export default function StatsGrid() {
  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
      {CARDS.map((card) => {
        const Icon = card.icon;

        return (
          <div
            key={card.label}
            className="rounded-xl border border-[#D9E2EC] bg-white p-5 shadow-sm"
          >
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm font-medium text-[#627D98]">
                  {card.label}
                </p>

                <h3 className="mt-2 text-3xl font-bold text-[#102A43]">
                  {card.value}
                </h3>

                <p className="mt-2 text-xs text-[#829AB1]">
                  {card.hint}
                </p>
              </div>

              <div
                className={`flex h-11 w-11 shrink-0 items-center justify-center rounded-full ${card.bg}`}
              >
                <Icon className={`h-5 w-5 ${card.color}`} />
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}

