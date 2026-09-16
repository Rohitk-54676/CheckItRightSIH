// "use client";

// import { CheckCircle2, Upload, FilePlus2 } from "lucide-react";
// import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

// type ActivityItem = {
//   id: string;
//   tone: "green" | "blue" | "amber";
//   title: string;
//   detail: string;
//   time: string;
// };

// const TONE_STYLES = {
//   green: { bg: "bg-[#DCFCE7]", icon: "text-[#16A34A]", Icon: CheckCircle2 },
//   blue: { bg: "bg-[#EAF4FF]", icon: "text-[#1769AA]", Icon: Upload },
//   amber: { bg: "bg-[#FEF3C7]", icon: "text-[#B45309]", Icon: FilePlus2 },
// } as const;

// export default function RecentActivity({
//   activity,
// }: {
//   activity: ActivityItem[];
// }) {
//   return (
//     <Card className="h-full">
//       <CardHeader className="flex-row items-center justify-between space-y-0">
//         <CardTitle className="text-sm font-semibold text-[#102A43]">
//           Recent Activity
//         </CardTitle>
//         <button
//           type="button"
//           className="text-xs font-semibold text-[#1769AA] hover:underline"
//         >
//           View all →
//         </button>
//       </CardHeader>

//       <CardContent className="flex flex-col gap-3">
//         {activity.length === 0 ? (
//           <p className="py-6 text-center text-xs text-[#627D98]">
//             No recent activity yet.
//           </p>
//         ) : (
//           activity.map((item) => {
//             const { bg, icon, Icon } = TONE_STYLES[item.tone];
//             return (
//               <div key={item.id} className="flex items-start gap-3">
//                 <span
//                   className={`flex h-7 w-7 shrink-0 items-center justify-center rounded-lg ${bg}`}
//                 >
//                   <Icon className={`h-3.5 w-3.5 ${icon}`} />
//                 </span>
//                 <div className="flex flex-1 flex-col gap-0.5">
//                   <span className="text-xs font-semibold text-[#102A43]">
//                     {item.title}
//                   </span>
//                   <span className="text-[11px] text-[#627D98]">
//                     {item.detail}
//                   </span>
//                 </div>
//                 <span className="shrink-0 text-[10px] text-[#627D98]">
//                   {item.time}
//                 </span>
//               </div>
//             );
//           })
//         )}
//       </CardContent>
//     </Card>
//   );
// }




"use client";

import { CheckCircle2, Upload, FilePlus2, Activity } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

type ActivityItem = {
  id: string;
  tone: "green" | "blue" | "amber";
  title: string;
  detail: string;
  time: string;
};

const TONE_STYLES = {
  green: {
    bg: "bg-[#16A34A]/10",
    ring: "ring-[#16A34A]/20",
    icon: "text-[#16A34A]",
    Icon: CheckCircle2,
  },
  blue: {
    bg: "bg-[#EAF4FF]",
    ring: "ring-[#1769AA]/20",
    icon: "text-[#1769AA]",
    Icon: Upload,
  },
  amber: {
    bg: "bg-[#F59E0B]/10",
    ring: "ring-[#F59E0B]/20",
    icon: "text-[#F59E0B]",
    Icon: FilePlus2,
  },
} as const;

export default function RecentActivity({
  activity,
}: {
  activity: ActivityItem[];
}) {
  return (
    <Card className="h-full transition-shadow duration-300 hover:shadow-[0_8px_24px_rgba(16,42,67,0.06)]">
      <CardHeader className="flex-row items-center justify-between space-y-0">
        <CardTitle className="text-sm font-semibold text-[#102A43]">
          Recent Activity
        </CardTitle>
        <button
          type="button"
          className="text-xs font-semibold text-[#1769AA] transition-colors hover:text-[#0B1F33] hover:underline"
        >
          View all →
        </button>
      </CardHeader>

      <CardContent className="flex flex-col gap-1">
        {activity.length === 0 ? (
          <div className="flex flex-col items-center gap-2 py-8">
            <span className="flex h-10 w-10 items-center justify-center rounded-full bg-[#EAF4FF]">
              <Activity className="h-5 w-5 text-[#1769AA]" />
            </span>
            <p className="text-center text-xs text-[#627D98]">
              No recent activity yet.
            </p>
          </div>
        ) : (
          activity.map((item, i) => {
            const { bg, ring, icon, Icon } = TONE_STYLES[item.tone];
            const isLast = i === activity.length - 1;
            return (
              <div key={item.id} className="relative flex gap-3">
                {/* Timeline connector */}
                {!isLast && (
                  <span className="absolute left-[13px] top-9 h-[calc(100%-12px)] w-px bg-[#D9E2EC]" />
                )}

                <span
                  className={`relative flex h-7 w-7 shrink-0 items-center justify-center rounded-lg ring-2 ${bg} ${ring}`}
                >
                  <Icon className={`h-3.5 w-3.5 ${icon}`} />
                </span>

                <div className="flex flex-1 flex-col gap-0.5 pb-3">
                  <div className="flex items-start justify-between gap-2">
                    <span className="text-xs font-semibold text-[#102A43]">
                      {item.title}
                    </span>
                    <span className="shrink-0 text-[10px] font-medium text-[#627D98]">
                      {item.time}
                    </span>
                  </div>
                  <span className="text-[11px] leading-snug text-[#627D98]">
                    {item.detail}
                  </span>
                </div>
              </div>
            );
          })
        )}
      </CardContent>
    </Card>
  );
}