// "use client";

// import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

// export default function TodaysSchedule() {
//   return (
//     <Card className="h-full">
//       <CardHeader className="flex-row items-center justify-between space-y-0">
//         <CardTitle className="text-sm font-semibold text-[#102A43]">
//           Today&apos;s Schedule
//         </CardTitle>
//       </CardHeader>

//       <CardContent className="flex items-center justify-center py-10">
//         <p className="text-center text-xs text-[#627D98]">
//           No inspections scheduled for today.
//         </p>
//       </CardContent>
//     </Card>
//   );
// }




"use client";

import { CalendarDays, Clock } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function TodaysSchedule() {
  return (
    <Card className="h-full transition-shadow duration-300 hover:shadow-[0_8px_24px_rgba(16,42,67,0.06)]">
      <CardHeader className="flex-row items-center justify-between space-y-0">
        <CardTitle className="text-sm font-semibold text-[#102A43]">
          Today&apos;s Schedule
        </CardTitle>
        <span className="flex items-center gap-1.5 rounded-full bg-[#EAF4FF] px-2.5 py-1 text-[10px] font-semibold text-[#1769AA]">
          <Clock className="h-3 w-3" />
          Today
        </span>
      </CardHeader>

      <CardContent className="flex items-center justify-center py-12">
        <div className="flex flex-col items-center gap-3 text-center">
          <span className="flex h-14 w-14 items-center justify-center rounded-full bg-[#EAF4FF] ring-8 ring-[#EAF4FF]/40">
            <CalendarDays className="h-6 w-6 text-[#1769AA]" />
          </span>
          <div className="flex flex-col gap-1">
            <p className="text-sm font-semibold text-[#102A43]">
              All clear for today
            </p>
            <p className="text-xs text-[#627D98]">
              No inspections scheduled for today.
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}