// "use client";

// import Link from "next/link";
// import Image from "next/image";
// import { usePathname } from "next/navigation";
// import {
//   LayoutDashboard,
//   ScanLine,
//   ClipboardList,
//   Loader,
//   History,
//   Package,
//   Bell,
//   User,
//   Settings,
//   ShieldCheck,
// } from "lucide-react";
// import { cn } from "@/lib/utils";

// const NAV_ITEMS = [
//   { href: "/inspector",               label: "Dashboard",          icon: LayoutDashboard },
//   { href: "/scan",                    label: "Scan Product",       icon: ScanLine },
//   { href: "/inspector/available",     label: "Available Cases",    icon: ClipboardList },
//   { href: "/inspector/my-cases",      label: "My Cases",           icon: Loader },
//   { href: "/inspector/history",       label: "Inspection History", icon: History },
//   { href: "/inspector/products",      label: "Products",           icon: Package },
//   { href: "/inspector/notifications", label: "Notifications",      icon: Bell },
//   { href: "/inspector/profile",       label: "Profile",            icon: User },
//   { href: "/inspector/settings",      label: "Settings",           icon: Settings },
// ];

// export default function InspectorSidebar() {
//   const pathname = usePathname();

//   return (
//     <aside className="hidden w-64 shrink-0 flex-col bg-[#0B1F33] lg:flex">
//       {/* Logo */}
//       <div className="flex h-16 items-center gap-2.5 border-b border-white/10 px-5">
//         <span className="relative flex h-9 w-9 shrink-0 items-center justify-center overflow-hidden rounded-xl border border-white/10 bg-white/5 p-1.5">
//           <Image
//             src="/images/logo.png"
//             alt="CheckItRight"
//             fill
//             sizes="36px"
//             className="object-contain"
//           />
//         </span>
//         <div className="flex flex-col leading-tight">
//           <span className="text-sm font-bold text-white">
//             CheckIt<span className="text-[#1769AA]">Right</span>
//           </span>
//           <span className="text-[10px] font-medium uppercase tracking-[0.14em] text-white/50">
//             Inspector Panel
//           </span>
//         </div>
//       </div>

//       {/* Nav */}
//       <nav className="flex-1 overflow-y-auto px-3 py-4">
//         <ul className="flex flex-col gap-1">
//           {NAV_ITEMS.map((item) => {
//             const Icon = item.icon;
//             const isActive =
//               item.href === "/inspector"
//                 ? pathname === "/inspector"
//                 : pathname?.startsWith(item.href);

//             return (
//               <li key={item.label}>
//                 <Link
//                   href={item.href}
//                   className={cn(
//                     "group relative flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors",
//                     isActive
//                       ? "bg-[#1769AA] text-white shadow-[0_6px_18px_rgba(23,105,170,0.35)]"
//                       : "text-white/70 hover:bg-white/5 hover:text-white",
//                   )}
//                 >
//                   <Icon className="h-4 w-4 shrink-0" />
//                   <span className="flex-1">{item.label}</span>
//                 </Link>
//               </li>
//             );
//           })}
//         </ul>
//       </nav>

//       {/* Footer badge */}
//       <div className="border-t border-white/10 p-4">
//         <div className="flex items-start gap-3 rounded-xl bg-white/5 p-3">
//           <ShieldCheck className="mt-0.5 h-4 w-4 shrink-0 text-[#16A34A]" />
//           <div className="flex flex-col gap-0.5">
//             <span className="text-xs font-semibold text-white">
//               Consumer Protection
//             </span>
//             <span className="text-[10px] leading-tight text-white/50">
//               Fair Trade · A Stronger India
//             </span>
//           </div>
//         </div>
//       </div>
//     </aside>
//   );
// }




"use client";

import Link from "next/link";
import Image from "next/image";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  ScanLine,
  ClipboardList,
  Loader,
  History,
  Package,
  Bell,
  User,
  Settings,
  ShieldCheck,
} from "lucide-react";
import { cn } from "@/lib/utils";

const NAV_ITEMS = [
  { href: "/inspector",               label: "Dashboard",          icon: LayoutDashboard },
  { href: "/scan",                    label: "Scan Product",       icon: ScanLine },
  { href: "/inspector/available",     label: "Available Cases",    icon: ClipboardList },
  { href: "/inspector/my-cases",      label: "My Cases",           icon: Loader },
  { href: "/inspector/history",       label: "Inspection History", icon: History },
  { href: "/inspector/products",      label: "Products",           icon: Package },
  { href: "/inspector/notifications", label: "Notifications",      icon: Bell },
  { href: "/inspector/profile",       label: "Profile",            icon: User },
  { href: "/inspector/settings",      label: "Settings",           icon: Settings },
];

export default function InspectorSidebar() {
  const pathname = usePathname();

  return (
    <aside className="sticky top-0 hidden h-screen w-64 shrink-0 flex-col overflow-hidden bg-[#0B1F33] lg:flex">
      {/* Subtle top glow (premium feel, same theme) */}
      <div className="pointer-events-none absolute left-0 top-0 h-40 w-full bg-gradient-to-b from-[#1769AA]/10 to-transparent" />

      {/* Logo */}
      <div className="relative flex h-16 shrink-0 items-center gap-2.5 border-b border-white/10 px-5">
        <span className="relative flex h-9 w-9 shrink-0 items-center justify-center overflow-hidden rounded-xl border border-white/10 bg-white/5 p-1.5">
          <Image
            src="/images/logo.png"
            alt="CheckItRight"
            fill
            sizes="36px"
            className="object-contain"
          />
        </span>
        <div className="flex flex-col leading-tight">
          <span className="text-sm font-bold text-white">
            CheckIt<span className="text-[#1769AA]">Right</span>
          </span>
          <span className="text-[10px] font-medium uppercase tracking-[0.14em] text-white/50">
            Inspector Panel
          </span>
        </div>
      </div>

      {/* Nav — this part scrolls if many items, but sidebar itself is fixed */}
      <nav className="relative flex-1 overflow-y-auto px-3 py-4">
        {/* Section label */}
        <p className="px-3 pb-2 text-[10px] font-bold uppercase tracking-[0.14em] text-white/30">
          Workspace
        </p>

        <ul className="flex flex-col gap-0.5">
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            const isActive =
              item.href === "/inspector"
                ? pathname === "/inspector"
                : pathname?.startsWith(item.href);

            return (
              <li key={item.label}>
                <Link
                  href={item.href}
                  className={cn(
                    "group relative flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-all duration-200",
                    isActive
                      ? "bg-[#1769AA] text-white shadow-[0_8px_22px_rgba(23,105,170,0.35)]"
                      : "text-white/65 hover:bg-white/5 hover:text-white hover:translate-x-0.5",
                  )}
                >
                  {/* Active left indicator */}
                  {isActive && (
                    <span className="absolute -left-3 top-1/2 h-6 w-1 -translate-y-1/2 rounded-r-full bg-[#16A34A] shadow-[0_0_8px_rgba(22,163,74,0.5)]" />
                  )}

                  <Icon
                    className={cn(
                      "h-4 w-4 shrink-0 transition-transform duration-200",
                      !isActive && "group-hover:scale-110",
                    )}
                  />
                  <span className="flex-1">{item.label}</span>
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>

      {/* Footer badge — always visible at bottom */}
      <div className="relative shrink-0 border-t border-white/10 p-4">
        <div className="flex items-start gap-3 rounded-xl bg-gradient-to-br from-white/[0.07] to-white/[0.02] p-3 ring-1 ring-inset ring-white/5">
          <ShieldCheck className="mt-0.5 h-4 w-4 shrink-0 text-[#16A34A]" />
          <div className="flex flex-col gap-0.5">
            <span className="text-xs font-semibold text-white">
              Consumer Protection
            </span>
            <span className="text-[10px] leading-tight text-white/50">
              Fair Trade · A Stronger India
            </span>
          </div>
        </div>
      </div>
    </aside>
  );
}