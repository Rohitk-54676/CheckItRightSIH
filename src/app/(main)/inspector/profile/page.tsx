// import { getInspectorProfile } from "@/lib/inspector/get-inspector-profile";

// const ROLE_LABEL: Record<string, string> = {
//   CONSUMER: "Consumer",
//   REVIEWER: "Reviewer",
//   INSPECTOR: "Inspector",
//   ADMIN: "Admin",
// };

// function initialsFrom(name: string) {
//   const parts = name.trim().split(/\s+/).filter(Boolean);
//   if (parts.length === 0) return "?";
//   if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
//   return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
// }

// function fmtDate(iso: string) {
//   return new Date(iso).toLocaleDateString("en-IN", {
//     day: "2-digit",
//     month: "short",
//     year: "numeric",
//   });
// }

// export default async function InspectorProfilePage() {
//   const profile = await getInspectorProfile();
//   const initials = initialsFrom(profile.name);

//   return (
//     <div className="mx-auto max-w-2xl space-y-4">
//       <div>
//         <h1 className="text-2xl font-bold text-[#102A43]">Profile</h1>
//         <p className="text-sm text-[#627D98] mt-1">
//           Your account information.
//         </p>
//       </div>

//       <div className="bg-white rounded-2xl border border-[#D9E2EC] p-6">
//         {/* Avatar + name */}
//         <div className="flex items-center gap-4 pb-6 border-b border-[#EAF0F6]">
//           {profile.imageUrl ? (
//             // eslint-disable-next-line @next/next/no-img-element
//             <img
//               src={profile.imageUrl}
//               alt={profile.name}
//               className="w-16 h-16 rounded-full object-cover"
//             />
//           ) : (
//             <div className="w-16 h-16 rounded-full bg-gradient-to-br from-[#1769AA] to-[#0B1F33] flex items-center justify-center text-white text-xl font-semibold">
//               {initials}
//             </div>
//           )}
//           <div className="min-w-0">
//             <p className="text-lg font-bold text-[#102A43] truncate">
//               {profile.name}
//             </p>
//             <p className="text-sm text-[#627D98] truncate">
//               {profile.email}
//             </p>
//             <span className="inline-flex mt-2 items-center px-2.5 py-1 rounded-full text-[11px] font-bold bg-[#EAF4FF] text-[#1769AA]">
//               {ROLE_LABEL[profile.role] ?? profile.role}
//             </span>
//           </div>
//         </div>

//         {/* Account */}
//         <dl className="mt-6 space-y-4">
//           <Row label="Role" value={ROLE_LABEL[profile.role] ?? profile.role} />
//           <Row
//             label="Status"
//             value={profile.status === "ACTIVE" ? "Active" : "Inactive"}
//           />
//           <Row label="Member since" value={fmtDate(profile.createdAt)} />
//           <Row
//             label="User ID"
//             value={<span className="font-mono text-xs">{profile.id}</span>}
//           />
//         </dl>

//         {/* Activity */}
//         <div className="mt-6 pt-6 border-t border-[#EAF0F6]">
//           <h2 className="text-[11px] font-bold uppercase tracking-wider text-[#627D98] mb-3">
//             Activity
//           </h2>
//           <div className="grid grid-cols-3 gap-3">
//             <Stat label="Claimed cases" value={profile.claimedCases} />
//             <Stat label="Completed" value={profile.completedCases} />
//             <Stat label="Violations" value={profile.violationsFound} />
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }

// function Row({
//   label,
//   value,
// }: {
//   label: string;
//   value: React.ReactNode;
// }) {
//   return (
//     <div className="flex items-start justify-between gap-4">
//       <dt className="text-sm text-[#627D98]">{label}</dt>
//       <dd className="text-sm font-medium text-[#102A43] text-right">
//         {value}
//       </dd>
//     </div>
//   );
// }

// function Stat({ label, value }: { label: string; value: number }) {
//   return (
//     <div className="rounded-xl bg-[#F7FAFC] border border-[#EAF0F6] p-3 text-center">
//       <p className="text-lg font-bold text-[#102A43]">{value}</p>
//       <p className="text-[10px] text-[#627D98] mt-0.5">{label}</p>
//     </div>
//   );
// }





import { getInspectorProfile } from "@/lib/inspector/get-inspector-profile";
import {
  ShieldCheck,
  Mail,
  CalendarDays,
  Fingerprint,
  ClipboardList,
  CheckCircle2,
  AlertTriangle,
  BadgeCheck,
} from "lucide-react";

const ROLE_LABEL: Record<string, string> = {
  CONSUMER: "Consumer",
  REVIEWER: "Reviewer",
  INSPECTOR: "Inspector",
  ADMIN: "Admin",
};

function initialsFrom(name: string) {
  const parts = name.trim().split(/\s+/).filter(Boolean);
  if (parts.length === 0) return "?";
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
}

function fmtDate(iso: string) {
  return new Date(iso).toLocaleDateString("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
}

export default async function InspectorProfilePage() {
  const profile = await getInspectorProfile();
  const initials = initialsFrom(profile.name);

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-[#102A43]">
          Profile
        </h1>
        <p className="mt-1 text-sm text-[#627D98]">
          Your account information and activity.
        </p>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* LEFT — Identity card */}
        {/* LEFT — Identity card */}
        {/* LEFT — Identity card */}
        <div className="lg:col-span-1">
          <div className="relative rounded-2xl border border-[#D9E2EC] bg-white shadow-[0_1px_2px_rgba(16,42,67,0.04)]">
            {/* Top navy banner */}
            <div className="relative h-24 overflow-hidden rounded-t-2xl bg-gradient-to-br from-[#0B1F33] via-[#0B1F33] to-[#1769AA]">
              <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(23,105,170,0.4),transparent_60%)]" />
            </div>

            {/* Avatar — fully OUTSIDE the banner, overlaps downward */}
            <div className="flex justify-center -mt-12">
              <div className="relative">
                {profile.imageUrl ? (
                  // eslint-disable-next-line @next/next/no-img-element
                  <img
                    src={profile.imageUrl}
                    alt={profile.name}
                    className="h-24 w-24 rounded-full object-cover ring-4 ring-white shadow-[0_6px_20px_rgba(16,42,67,0.15)]"
                  />
                ) : (
                  <div className="flex h-24 w-24 items-center justify-center rounded-full bg-gradient-to-br from-[#1769AA] to-[#0B1F33] text-2xl font-bold text-white ring-4 ring-white shadow-[0_6px_20px_rgba(16,42,67,0.15)]">
                    {initials}
                  </div>
                )}
                {/* Online indicator */}
                <span className="absolute bottom-1 right-1 h-4 w-4 rounded-full border-2 border-white bg-[#16A34A]" />
              </div>
            </div>

            {/* Name + email + pills — centered */}
            <div className="flex flex-col items-center px-6 pb-6 pt-4 text-center">
              <h2 className="truncate text-lg font-bold text-[#102A43]">
                {profile.name}
              </h2>
              <div className="mt-1 flex items-center gap-1.5 text-sm text-[#627D98]">
                <Mail className="h-3.5 w-3.5 shrink-0" />
                <span className="truncate">{profile.email}</span>
              </div>

              <div className="mt-4 flex flex-wrap items-center justify-center gap-2">
                <span className="inline-flex items-center gap-1.5 rounded-full bg-[#EAF4FF] px-2.5 py-1 text-[11px] font-semibold text-[#1769AA]">
                  <BadgeCheck className="h-3 w-3" />
                  {ROLE_LABEL[profile.role] ?? profile.role}
                </span>
                <span
                  className={
                    profile.status === "ACTIVE"
                      ? "inline-flex items-center gap-1.5 rounded-full bg-[#16A34A]/10 px-2.5 py-1 text-[11px] font-semibold text-[#16A34A]"
                      : "inline-flex items-center gap-1.5 rounded-full bg-[#DC2626]/10 px-2.5 py-1 text-[11px] font-semibold text-[#DC2626]"
                  }
                >
                  <span
                    className={
                      profile.status === "ACTIVE"
                        ? "h-1.5 w-1.5 rounded-full bg-[#16A34A]"
                        : "h-1.5 w-1.5 rounded-full bg-[#DC2626]"
                    }
                  />
                  {profile.status === "ACTIVE" ? "Active" : "Inactive"}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* RIGHT — Details + Activity */}
        <div className="space-y-6 lg:col-span-2">
          {/* Account details */}
          <div className="rounded-2xl border border-[#D9E2EC] bg-white shadow-[0_1px_2px_rgba(16,42,67,0.04)]">
            <div className="flex items-center gap-2 border-b border-[#EAF0F6] px-6 py-4">
              <ShieldCheck className="h-4 w-4 text-[#1769AA]" />
              <h3 className="text-sm font-bold text-[#102A43]">
                Account details
              </h3>
            </div>

            <dl className="divide-y divide-[#EAF0F6]">
              <Row
                icon={<BadgeCheck className="h-3.5 w-3.5" />}
                label="Role"
                value={ROLE_LABEL[profile.role] ?? profile.role}
              />
              <Row
                icon={<ShieldCheck className="h-3.5 w-3.5" />}
                label="Status"
                value={profile.status === "ACTIVE" ? "Active" : "Inactive"}
              />
              <Row
                icon={<CalendarDays className="h-3.5 w-3.5" />}
                label="Member since"
                value={fmtDate(profile.createdAt)}
              />
              <Row
                icon={<Fingerprint className="h-3.5 w-3.5" />}
                label="User ID"
                value={
                  <span className="font-mono text-[11px] text-[#627D98]">
                    {profile.id}
                  </span>
                }
              />
            </dl>
          </div>

          {/* Activity */}
          <div className="rounded-2xl border border-[#D9E2EC] bg-white shadow-[0_1px_2px_rgba(16,42,67,0.04)]">
            <div className="flex items-center gap-2 border-b border-[#EAF0F6] px-6 py-4">
              <ClipboardList className="h-4 w-4 text-[#1769AA]" />
              <h3 className="text-sm font-bold text-[#102A43]">Activity</h3>
            </div>

            <div className="grid grid-cols-1 gap-3 p-6 sm:grid-cols-3">
              <StatCard
                icon={<ClipboardList className="h-4 w-4" />}
                label="Claimed cases"
                value={profile.claimedCases}
                tone="blue"
              />
              <StatCard
                icon={<CheckCircle2 className="h-4 w-4" />}
                label="Completed"
                value={profile.completedCases}
                tone="green"
              />
              <StatCard
                icon={<AlertTriangle className="h-4 w-4" />}
                label="Violations"
                value={profile.violationsFound}
                tone="red"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

/* -------------------------------------------------------
   Row — key/value line in Account details
------------------------------------------------------- */

function Row({
  icon,
  label,
  value,
}: {
  icon: React.ReactNode;
  label: string;
  value: React.ReactNode;
}) {
  return (
    <div className="flex items-center justify-between gap-4 px-6 py-4 transition-colors hover:bg-[#F7FAFC]">
      <dt className="flex items-center gap-2.5 text-sm text-[#627D98]">
        <span className="text-[#829AB1]">{icon}</span>
        {label}
      </dt>
      <dd className="text-right text-sm font-semibold text-[#102A43]">
        {value}
      </dd>
    </div>
  );
}

/* -------------------------------------------------------
   StatCard — activity metric
------------------------------------------------------- */

const TONE_STYLES = {
  blue: { bg: "bg-[#EAF4FF]", icon: "text-[#1769AA]", ring: "ring-[#1769AA]/10" },
  green: { bg: "bg-[#16A34A]/10", icon: "text-[#16A34A]", ring: "ring-[#16A34A]/10" },
  red: { bg: "bg-[#DC2626]/10", icon: "text-[#DC2626]", ring: "ring-[#DC2626]/10" },
} as const;

function StatCard({
  icon,
  label,
  value,
  tone,
}: {
  icon: React.ReactNode;
  label: string;
  value: number;
  tone: keyof typeof TONE_STYLES;
}) {
  const t = TONE_STYLES[tone];
  return (
    <div className="group relative overflow-hidden rounded-xl border border-[#D9E2EC] bg-white p-4 transition-all duration-300 hover:-translate-y-0.5 hover:border-[#1769AA]/30 hover:shadow-[0_8px_24px_rgba(23,105,170,0.08)]">
      <div className="flex items-center gap-2">
        <span
          className={`flex h-8 w-8 items-center justify-center rounded-lg ring-2 ${t.bg} ${t.ring}`}
        >
          <span className={t.icon}>{icon}</span>
        </span>
        <span className="text-[11px] font-semibold uppercase tracking-wide text-[#627D98]">
          {label}
        </span>
      </div>
      <p className="mt-3 text-2xl font-bold leading-none tracking-tight text-[#102A43]">
        {value}
      </p>
    </div>
  );
}