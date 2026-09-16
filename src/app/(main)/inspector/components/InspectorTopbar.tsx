// "use client";

// import { Search, Bell, ChevronDown, LogOut, Menu } from "lucide-react";
// import { useClerk } from "@clerk/nextjs";
// import { useRouter } from "next/navigation";

// type Props = {
//   onOpenMenu: () => void;
//   name: string;
//   role: string;
//   imageUrl?: string | null;
// };

// function initialsFrom(name: string) {
//   const parts = name.trim().split(/\s+/).filter(Boolean);
//   if (parts.length === 0) return "?";
//   if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
//   return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
// }

// function roleLabel(role: string) {
//   const map: Record<string, string> = {
//     CONSUMER: "Consumer",
//     REVIEWER: "Reviewer",
//     INSPECTOR: "Field Inspector",
//     ADMIN: "Admin",
//   };
//   return map[role] ?? role;
// }

// export default function InspectorTopbar({
//   onOpenMenu,
//   name,
//   role,
//   imageUrl,
// }: Props) {
//   const { signOut } = useClerk();
//   const router = useRouter();
//   const initials = initialsFrom(name);

//   const handleLogout = async () => {
//     await signOut();
//     router.push("/");
//   };

//   return (
//     <header className="sticky top-0 z-30 flex h-16 items-center gap-3 border-b border-[#D9E2EC] bg-white/95 px-4 backdrop-blur-xl sm:gap-4 sm:px-6">
//       {/* Hamburger (mobile only) */}
//       <button
//         type="button"
//         onClick={onOpenMenu}
//         aria-label="Open menu"
//         className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl border border-[#D9E2EC] bg-white text-[#102A43] transition-colors hover:bg-[#EAF4FF] lg:hidden"
//       >
//         <Menu className="h-4 w-4" />
//       </button>

//       {/* Search */}
//       <div className="relative hidden flex-1 max-w-md sm:block">
//         <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-[#627D98]" />
//         <input
//           type="text"
//           placeholder="Search cases, products, shops, locations..."
//           className="h-10 w-full rounded-xl border border-[#D9E2EC] bg-[#F7FAFC] pl-9 pr-3 text-sm text-[#102A43] placeholder:text-[#627D98]/70 outline-none transition-colors focus:border-[#1769AA] focus:bg-white"
//         />
//       </div>

//       {/* Mobile brand */}
//       <div className="flex flex-1 items-center gap-2 sm:hidden">
//         <span className="text-sm font-bold text-[#102A43]">
//           CheckIt<span className="text-[#1769AA]">Right</span>
//         </span>
//       </div>

//       <div className="flex shrink-0 items-center gap-2 sm:gap-3">
//         {/* Notification */}
//         <button
//           type="button"
//           aria-label="Notifications"
//           className="relative flex h-10 w-10 items-center justify-center rounded-xl border border-[#D9E2EC] bg-white text-[#102A43] transition-colors hover:bg-[#EAF4FF]"
//         >
//           <Bell className="h-4 w-4" />
//           <span className="absolute right-2 top-2 h-2 w-2 rounded-full bg-[#DC2626]" />
//         </button>

//         {/* User chip */}
//         <button
//           type="button"
//           className="flex items-center gap-3 rounded-xl border border-[#D9E2EC] bg-white px-1.5 py-1.5 transition-colors hover:bg-[#EAF4FF] sm:px-2"
//         >
//           {imageUrl ? (
//             // eslint-disable-next-line @next/next/no-img-element
//             <img
//               src={imageUrl}
//               alt={name}
//               className="h-8 w-8 shrink-0 rounded-lg object-cover"
//             />
//           ) : (
//             <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-[#1769AA] text-xs font-bold text-white">
//               {initials}
//             </span>
//           )}
//           <span className="hidden flex-col items-start leading-tight sm:flex">
//             <span className="text-xs font-semibold text-[#102A43]">
//               {name}
//             </span>
//             <span className="text-[10px] text-[#627D98]">
//               {roleLabel(role)}
//             </span>
//           </span>
//           <ChevronDown className="hidden h-3.5 w-3.5 text-[#627D98] sm:block" />
//         </button>

//         {/* Logout */}
//         <button
//           type="button"
//           onClick={handleLogout}
//           aria-label="Logout"
//           className="group flex h-10 items-center gap-2 rounded-xl border border-[#DC2626]/20 bg-white px-2.5 text-[#DC2626] transition-colors hover:bg-[#DC2626]/10 sm:px-3"
//         >
//           <LogOut className="h-4 w-4 transition-transform group-hover:-translate-x-0.5" />
//           <span className="hidden text-xs font-semibold sm:inline">
//             Logout
//           </span>
//         </button>
//       </div>
//     </header>
//   );
// }


"use client";

import { Search, Bell, ChevronDown, LogOut, Menu } from "lucide-react";
import { useClerk } from "@clerk/nextjs";
import { useRouter } from "next/navigation";

type Props = {
  onOpenMenu: () => void;
  name: string;
  role: string;
  imageUrl?: string | null;
};

function initialsFrom(name: string) {
  const parts = name.trim().split(/\s+/).filter(Boolean);
  if (parts.length === 0) return "?";
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
}

function roleLabel(role: string) {
  const map: Record<string, string> = {
    CONSUMER: "Consumer",
    REVIEWER: "Reviewer",
    INSPECTOR: "Field Inspector",
    ADMIN: "Admin",
  };
  return map[role] ?? role;
}

export default function InspectorTopbar({
  onOpenMenu,
  name,
  role,
  imageUrl,
}: Props) {
  const { signOut } = useClerk();
  const router = useRouter();
  const initials = initialsFrom(name);

  const handleLogout = async () => {
    await signOut();
    router.push("/");
  };

  return (
    <header className="sticky top-0 z-30 border-b border-[#D9E2EC] bg-white/80 backdrop-blur-xl">
      <div className="flex h-16 items-center gap-3 px-4 sm:gap-4 sm:px-6">
        {/* Hamburger (mobile only) */}
        <button
          type="button"
          onClick={onOpenMenu}
          aria-label="Open menu"
          className="group flex h-10 w-10 shrink-0 items-center justify-center rounded-xl border border-[#D9E2EC] bg-white text-[#102A43] shadow-[0_1px_2px_rgba(16,42,67,0.04)] transition-all hover:border-[#1769AA]/30 hover:bg-[#EAF4FF] hover:shadow-[0_4px_12px_rgba(23,105,170,0.08)] lg:hidden"
        >
          <Menu className="h-4 w-4 transition-transform group-hover:scale-110" />
        </button>

        {/* Search */}
        <div className="relative hidden flex-1 max-w-md sm:block">
          <Search className="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-[#627D98]" />
          <input
            type="text"
            placeholder="Search cases, products, shops, locations..."
            className="h-10 w-full rounded-xl border border-[#D9E2EC] bg-[#F7FAFC] pl-10 pr-3 text-sm text-[#102A43] placeholder:text-[#627D98]/70 outline-none transition-all focus:border-[#1769AA] focus:bg-white focus:shadow-[0_0_0_3px_rgba(23,105,170,0.08)]"
          />
          {/* Keyboard hint — subtle premium touch */}
          <kbd className="pointer-events-none absolute right-3 top-1/2 hidden -translate-y-1/2 rounded-md border border-[#D9E2EC] bg-white px-1.5 py-0.5 text-[10px] font-semibold text-[#627D98] lg:inline-block">
            ⌘K
          </kbd>
        </div>

        {/* Mobile brand */}
        <div className="flex flex-1 items-center gap-2 sm:hidden">
          <span className="text-sm font-bold text-[#102A43]">
            CheckIt<span className="text-[#1769AA]">Right</span>
          </span>
        </div>

        <div className="flex shrink-0 items-center gap-2 sm:gap-2.5">
          {/* Notification */}
          <button
            type="button"
            aria-label="Notifications"
            className="group relative flex h-10 w-10 items-center justify-center rounded-xl border border-[#D9E2EC] bg-white text-[#102A43] shadow-[0_1px_2px_rgba(16,42,67,0.04)] transition-all hover:border-[#1769AA]/30 hover:bg-[#EAF4FF] hover:shadow-[0_4px_12px_rgba(23,105,170,0.08)]"
          >
            <Bell className="h-4 w-4 transition-transform group-hover:scale-110" />
            {/* Unread dot — subtle pulse */}
            <span className="absolute right-2 top-2 flex h-2 w-2">
              <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-[#DC2626] opacity-60" />
              <span className="relative inline-flex h-2 w-2 rounded-full bg-[#DC2626]" />
            </span>
          </button>

          {/* User chip */}
          <button
            type="button"
            className="group flex items-center gap-2.5 rounded-xl border border-[#D9E2EC] bg-white py-1.5 pl-1.5 pr-2 shadow-[0_1px_2px_rgba(16,42,67,0.04)] transition-all hover:border-[#1769AA]/30 hover:bg-[#EAF4FF] hover:shadow-[0_4px_12px_rgba(23,105,170,0.08)] sm:pr-3"
          >
            {imageUrl ? (
              // eslint-disable-next-line @next/next/no-img-element
              <img
                src={imageUrl}
                alt={name}
                className="h-8 w-8 shrink-0 rounded-lg object-cover ring-1 ring-inset ring-black/5"
              />
            ) : (
              <span className="relative flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-gradient-to-br from-[#1769AA] to-[#0B1F33] text-xs font-bold text-white shadow-[inset_0_1px_0_rgba(255,255,255,0.15)]">
                {initials}
              </span>
            )}
            <span className="hidden flex-col items-start leading-tight sm:flex">
              <span className="text-xs font-semibold text-[#102A43]">
                {name}
              </span>
              <span className="text-[10px] text-[#627D98]">
                {roleLabel(role)}
              </span>
            </span>
            <ChevronDown className="hidden h-3.5 w-3.5 text-[#627D98] transition-transform group-hover:translate-y-0.5 sm:block" />
          </button>

          {/* Logout */}
          <button
            type="button"
            onClick={handleLogout}
            aria-label="Logout"
            className="group flex h-10 items-center gap-2 rounded-xl border border-[#DC2626]/15 bg-white px-2.5 text-[#DC2626] shadow-[0_1px_2px_rgba(16,42,67,0.04)] transition-all hover:border-[#DC2626]/30 hover:bg-[#DC2626]/[0.06] hover:shadow-[0_4px_12px_rgba(220,38,38,0.08)] sm:px-3"
          >
            <LogOut className="h-4 w-4 transition-transform group-hover:-translate-x-0.5" />
            <span className="hidden text-xs font-semibold sm:inline">
              Logout
            </span>
          </button>
        </div>
      </div>

      {/* Subtle bottom accent line — gives depth without changing theme */}
      <div className="h-px w-full bg-gradient-to-r from-transparent via-[#1769AA]/15 to-transparent" />
    </header>
  );
}