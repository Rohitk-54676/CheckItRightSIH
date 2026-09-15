
"use client";

import ReviewerSidebar from "./ReviewerSidebar";
import ReviewerTopbar from "./ReviewerTopbar";

export default function ReviewerShell({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-[#F7FAFC]">
      <ReviewerSidebar />

      <div className="ml-64 flex min-h-screen flex-col">
        <ReviewerTopbar />

        <main className="flex-1 p-4 lg:p-8">
          {children}
        </main>
      </div>
    </div>
  );
}

