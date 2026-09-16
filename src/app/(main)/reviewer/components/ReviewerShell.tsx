"use client";

import { useState, createContext, useContext } from "react";
import ReviewerSidebar from "./ReviewerSidebar";

type ReviewerUser = {
  name: string;
  email: string;
  role: string;
  imageUrl: string | null;
};

function ReviewerTopbar({
  name,
  role,
  imageUrl,
}: Pick<ReviewerUser, "name" | "role" | "imageUrl">) {
  return (
    <header className="flex items-center justify-between border-b border-gray-200 bg-white px-4 py-4 lg:px-8">
      <div>
        <h1 className="text-lg font-semibold text-gray-900">Reviewer Dashboard</h1>
        <p className="text-sm text-gray-500">{role}</p>
      </div>
      <div className="flex items-center gap-3">
        {imageUrl ? (
          <img src={imageUrl} alt={name} className="h-9 w-9 rounded-full object-cover" />
        ) : (
          <div className="flex h-9 w-9 items-center justify-center rounded-full bg-gray-200 text-sm font-medium text-gray-700">
            {name.charAt(0).toUpperCase()}
          </div>
        )}
        <span className="hidden text-sm font-medium text-gray-700 sm:block">{name}</span>
      </div>
    </header>
  );
}

type SidebarContextType = {
  collapsed: boolean;
  toggleCollapsed: () => void;
  mobileOpen: boolean;
  setMobileOpen: (open: boolean) => void;
};

const SidebarContext = createContext<SidebarContextType | null>(null);

export function useSidebar() {
  const ctx = useContext(SidebarContext);
  if (!ctx) throw new Error("useSidebar must be used within ReviewerShell");
  return ctx;
}

export default function ReviewerShell({
  user,
  children,
}: {
  user: ReviewerUser;
  children: React.ReactNode;
}) {
  const [collapsed, setCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  const toggleCollapsed = () => setCollapsed((c) => !c);

  return (
    <SidebarContext.Provider
      value={{ collapsed, toggleCollapsed, mobileOpen, setMobileOpen }}
    >
      <div className="min-h-screen bg-[#F7FAFC]">
        {/* Mobile overlay */}
        {mobileOpen && (
          <div
            className="fixed inset-0 z-30 bg-black/30 backdrop-blur-sm transition-opacity lg:hidden"
            onClick={() => setMobileOpen(false)}
          />
        )}

        {/* Sidebar wrapper handles the responsive/collapse transform;
            ReviewerSidebar itself renders content and can call useSidebar()
            for its own collapsed-state styling if desired */}
        <div
          className={`fixed inset-y-0 left-0 z-40 transition-transform duration-300 ease-in-out lg:translate-x-0 ${
            mobileOpen ? "translate-x-0" : "-translate-x-full"
          } ${collapsed ? "lg:w-20" : "lg:w-64"}`}
        >
          <ReviewerSidebar />
        </div>

        <div
          className={`flex min-h-screen flex-col transition-[margin] duration-300 ease-in-out ${
            collapsed ? "lg:ml-20" : "lg:ml-64"
          }`}
        >
          <ReviewerTopbar
            name={user.name}
            role={user.role}
            imageUrl={user.imageUrl}
          />
          <main className="flex-1 p-4 lg:p-8">{children}</main>
        </div>
      </div>
    </SidebarContext.Provider>
  );
}