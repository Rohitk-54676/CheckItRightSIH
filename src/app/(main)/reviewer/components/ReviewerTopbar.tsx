
"use client";

import { Bell, LogOut } from "lucide-react";

export default function ReviewerTopbar() {
  const name = "Kezhanguü Kruse";
  const role = "Reviewer";

  return (
    <header className="sticky top-0 z-30 flex h-16 items-center justify-between gap-4 border-b border-[#D9E2EC] bg-white/95 px-4 backdrop-blur-xl sm:px-6">
      
      {/* Page Title */}
      <div>
        <h1 className="text-lg font-bold text-[#102A43]">
          Reviewer Dashboard
        </h1>

        <p className="text-[11px] text-[#829AB1]">
          Review Reports • Verify Evidence • Ensure Compliance
        </p>
      </div>

      {/* Right Section */}
      <div className="flex shrink-0 items-center gap-2 sm:gap-3">
        
        {/* Notifications */}
        <button
          type="button"
          aria-label="Notifications"
          className="relative flex h-10 w-10 items-center justify-center rounded-xl border border-[#D9E2EC] bg-white text-[#102A43] transition-colors hover:bg-[#EAF4FF]"
        >
          <Bell className="h-4 w-4" />

          <span className="absolute right-2 top-2 h-1.5 w-1.5 rounded-full bg-[#DC2626]" />
        </button>

        {/* Reviewer Profile */}
        <button
          type="button"
          className="flex items-center gap-3 rounded-xl border border-[#D9E2EC] bg-white px-1.5 py-1.5 transition-colors hover:bg-[#EAF4FF] sm:px-2"
        >
          <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-[#1769AA] text-xs font-bold text-white">
            KK
          </span>

          <span className="hidden flex-col items-start leading-tight sm:flex">
            <span className="text-xs font-semibold text-[#102A43]">
              {name}
            </span>

            <span className="text-[10px] text-[#627D98]">
              {role}
            </span>
          </span>
        </button>

        {/* Logout */}
        <button
          type="button"
          aria-label="Logout"
          className="group flex h-10 items-center gap-2 rounded-xl border border-[#D9E2EC] bg-white px-3 text-[#102A43] transition-colors hover:bg-[#EAF4FF]"
        >
          <LogOut className="h-4 w-4" />
          <span className="hidden text-xs font-semibold sm:inline">Logout</span>
        </button>
      </div>
    </header>
  );
}

