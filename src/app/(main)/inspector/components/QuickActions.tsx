// "use client";

// import Link from "next/link";
// import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
// import { ScanLine, ClipboardList, History } from "lucide-react";

// const ACTIONS = [
//   {
//     href: "/scan",
//     label: "Scan Product",
//     hint: "Scan and verify product on-site",
//     Icon: ScanLine,
//   },
//   {
//     href: "/inspector/available",
//     label: "Available Cases",
//     hint: "View and claim forwarded cases",
//     Icon: ClipboardList,
//   },
//   {
//     href: "/inspector/history",
//     label: "Inspection History",
//     hint: "View completed inspections",
//     Icon: History,
//   },
// ];

// export default function QuickActions() {
//   return (
//     <Card>
//       <CardHeader className="flex-row items-center justify-between space-y-0">
//         <CardTitle className="text-sm font-semibold text-[#102A43]">
//           Quick Actions
//         </CardTitle>
//       </CardHeader>
//       <CardContent className="grid grid-cols-1 gap-3 sm:grid-cols-3">
//         {ACTIONS.map(({ href, label, hint, Icon }) => (
//           <Link
//             key={href}
//             href={href}
//             className="group flex items-start gap-3 rounded-xl border border-[#D9E2EC] p-4 transition hover:border-[#1769AA]/40 hover:bg-[#EAF4FF]/40"
//           >
//             <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-[#EAF4FF]">
//               <Icon className="h-4 w-4 text-[#1769AA]" />
//             </span>
//             <div className="min-w-0">
//               <p className="text-sm font-semibold text-[#102A43]">{label}</p>
//               <p className="mt-0.5 text-[11px] text-[#627D98]">{hint}</p>
//             </div>
//           </Link>
//         ))}
//       </CardContent>
//     </Card>
//   );
// }



"use client";

import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ScanLine, ClipboardList, History, ArrowUpRight } from "lucide-react";

const ACTIONS = [
  {
    href: "/scan",
    label: "Scan Product",
    hint: "Scan and verify product on-site",
    Icon: ScanLine,
    tone: "blue" as const,
  },
  {
    href: "/inspector/available",
    label: "Available Cases",
    hint: "View and claim forwarded cases",
    Icon: ClipboardList,
    tone: "amber" as const,
  },
  {
    href: "/inspector/history",
    label: "Inspection History",
    hint: "View completed inspections",
    Icon: History,
    tone: "green" as const,
  },
];

const TONES = {
  blue: { bg: "bg-[#EAF4FF]", icon: "text-[#1769AA]", hover: "group-hover:bg-[#1769AA] group-hover:text-white" },
  amber: { bg: "bg-[#F59E0B]/10", icon: "text-[#F59E0B]", hover: "group-hover:bg-[#F59E0B] group-hover:text-white" },
  green: { bg: "bg-[#16A34A]/10", icon: "text-[#16A34A]", hover: "group-hover:bg-[#16A34A] group-hover:text-white" },
};

export default function QuickActions() {
  return (
    <Card className="transition-shadow duration-300 hover:shadow-[0_8px_24px_rgba(16,42,67,0.06)]">
      <CardHeader className="flex-row items-center justify-between space-y-0">
        <CardTitle className="text-sm font-semibold text-[#102A43]">
          Quick Actions
        </CardTitle>
      </CardHeader>
      <CardContent className="grid grid-cols-1 gap-3 sm:grid-cols-3">
        {ACTIONS.map(({ href, label, hint, Icon, tone }) => {
          const t = TONES[tone];
          return (
            <Link
              key={href}
              href={href}
              className="group relative flex items-start gap-3 overflow-hidden rounded-xl border border-[#D9E2EC] bg-white p-4 transition-all duration-300 hover:-translate-y-0.5 hover:border-[#1769AA]/40 hover:shadow-[0_8px_24px_rgba(23,105,170,0.08)]"
            >
              <span
                className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-lg transition-colors duration-300 ${t.bg} ${t.hover}`}
              >
                <Icon className={`h-4 w-4 transition-colors duration-300 ${t.icon} group-hover:text-white`} />
              </span>

              <div className="min-w-0 flex-1">
                <p className="text-sm font-semibold text-[#102A43]">
                  {label}
                </p>
                <p className="mt-0.5 text-[11px] leading-snug text-[#627D98]">
                  {hint}
                </p>
              </div>

              <ArrowUpRight className="h-4 w-4 shrink-0 text-[#627D98]/50 transition-all duration-300 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 group-hover:text-[#1769AA]" />
            </Link>
          );
        })}
      </CardContent>
    </Card>
  );
}