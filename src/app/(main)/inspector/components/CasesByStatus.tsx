// "use client";

// import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

// type Segment = {
//   label: string;
//   value: number;
//   color: string;
// };

// export default function CasesByStatus({
//   segments,
//   total,
// }: {
//   segments: Segment[];
//   total: number;
// }) {
//   const size = 140;
//   const stroke = 16;
//   const radius = (size - stroke) / 2;
//   const circumference = 2 * Math.PI * radius;

//   const safeTotal = total > 0 ? total : 1;
//   let offset = 0;
//   const arcs = segments.map((seg) => {
//     const fraction = seg.value / safeTotal;
//     const dash = fraction * circumference;
//     const arc = { ...seg, dash, offset };
//     offset += dash;
//     return arc;
//   });

//   return (
//     <Card className="h-full">
//       <CardHeader className="flex-row items-center justify-between space-y-0">
//         <CardTitle className="text-sm font-semibold text-[#102A43]">
//           Cases by Status
//         </CardTitle>
//         <button
//           type="button"
//           className="text-xs font-semibold text-[#1769AA] hover:underline"
//         >
//           View all →
//         </button>
//       </CardHeader>

//       <CardContent className="flex flex-col items-center gap-4 sm:flex-row">
//         <div className="relative shrink-0">
//           <svg width={size} height={size} className="-rotate-90">
//             <circle
//               cx={size / 2}
//               cy={size / 2}
//               r={radius}
//               fill="none"
//               stroke="#EAF4FF"
//               strokeWidth={stroke}
//             />
//             {total > 0 &&
//               arcs.map((arc, i) => (
//                 <circle
//                   key={i}
//                   cx={size / 2}
//                   cy={size / 2}
//                   r={radius}
//                   fill="none"
//                   stroke={arc.color}
//                   strokeWidth={stroke}
//                   strokeDasharray={`${arc.dash} ${circumference - arc.dash}`}
//                   strokeDashoffset={-arc.offset}
//                   strokeLinecap="butt"
//                 />
//               ))}
//           </svg>

//           <div className="absolute inset-0 flex flex-col items-center justify-center">
//             <span className="text-2xl font-bold text-[#102A43]">{total}</span>
//             <span className="text-[10px] font-medium uppercase tracking-wider text-[#627D98]">
//               Total Cases
//             </span>
//           </div>
//         </div>

//         <ul className="flex w-full flex-col gap-2">
//           {segments.map((seg) => (
//             <li key={seg.label} className="flex items-center gap-2 text-xs">
//               <span
//                 className="h-2.5 w-2.5 shrink-0 rounded-full"
//                 style={{ background: seg.color }}
//               />
//               <span className="flex-1 text-[#102A43]">{seg.label}</span>
//               <span className="font-semibold text-[#102A43]">{seg.value}</span>
//             </li>
//           ))}
//         </ul>
//       </CardContent>
//     </Card>
//   );
// }



"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

type Segment = {
  label: string;
  value: number;
  color: string;
};

export default function CasesByStatus({
  segments,
  total,
}: {
  segments: Segment[];
  total: number;
}) {
  const size = 140;
  const stroke = 16;
  const radius = (size - stroke) / 2;
  const circumference = 2 * Math.PI * radius;

  const safeTotal = total > 0 ? total : 1;
  let offset = 0;
  const arcs = segments.map((seg) => {
    const fraction = seg.value / safeTotal;
    const dash = fraction * circumference;
    const arc = { ...seg, dash, offset };
    offset += dash;
    return arc;
  });

  return (
    <Card className="h-full transition-shadow duration-300 hover:shadow-[0_8px_24px_rgba(16,42,67,0.06)]">
      <CardHeader className="flex-row items-center justify-between space-y-0">
        <CardTitle className="text-sm font-semibold text-[#102A43]">
          Cases by Status
        </CardTitle>
        <button
          type="button"
          className="text-xs font-semibold text-[#1769AA] transition-colors hover:text-[#0B1F33] hover:underline"
        >
          View all →
        </button>
      </CardHeader>

      <CardContent className="flex flex-col items-center gap-4 sm:flex-row">
        <div className="relative shrink-0">
          {/* Soft outer glow ring */}
          <div className="absolute inset-0 -m-2 rounded-full bg-[#1769AA]/[0.03] blur-xl" />

          <svg width={size} height={size} className="relative -rotate-90">
            <circle
              cx={size / 2}
              cy={size / 2}
              r={radius}
              fill="none"
              stroke="#EAF4FF"
              strokeWidth={stroke}
            />
            {total > 0 &&
              arcs.map((arc, i) => (
                <circle
                  key={i}
                  cx={size / 2}
                  cy={size / 2}
                  r={radius}
                  fill="none"
                  stroke={arc.color}
                  strokeWidth={stroke}
                  strokeDasharray={`${arc.dash} ${circumference - arc.dash}`}
                  strokeDashoffset={-arc.offset}
                  strokeLinecap="butt"
                  className="transition-all duration-500"
                />
              ))}
          </svg>

          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className="text-3xl font-bold leading-none tracking-tight text-[#102A43]">
              {total}
            </span>
            <span className="mt-1 text-[10px] font-semibold uppercase tracking-[0.14em] text-[#627D98]">
              Total Cases
            </span>
          </div>
        </div>

        <ul className="flex w-full flex-col gap-2.5">
          {segments.map((seg) => (
            <li
              key={seg.label}
              className="group flex items-center gap-2.5 rounded-lg px-2 py-1.5 transition-colors hover:bg-[#F7FAFC]"
            >
              <span
                className="h-2.5 w-2.5 shrink-0 rounded-full ring-2 ring-white"
                style={{ background: seg.color }}
              />
              <span className="flex-1 text-xs font-medium text-[#102A43]">
                {seg.label}
              </span>
              <span className="text-xs font-bold tabular-nums text-[#102A43]">
                {seg.value}
              </span>
            </li>
          ))}
        </ul>
      </CardContent>
    </Card>
  );
}