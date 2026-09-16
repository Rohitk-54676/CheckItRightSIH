// "use client";

// import { useState } from "react";
// import InspectorSidebar from "./InspectorSidebar";
// import MobileDrawer from "./MobileDrawer";
// import MobileBottomNav from "./MobileBottomNav";
// import InspectorTopbar from "./InspectorTopbar";

// type InspectorUser = {
//   name: string;
//   email: string;
//   role: string;
//   imageUrl: string | null;
// };

// export default function InspectorShell({
//   user,
//   children,
// }: {
//   user: InspectorUser;
//   children: React.ReactNode;
// }) {
//   const [menuOpen, setMenuOpen] = useState(false);

//   return (
//     <div className="flex min-h-screen bg-[#F7FAFC]">
//       <InspectorSidebar />

//       <MobileDrawer open={menuOpen} onClose={() => setMenuOpen(false)} />

//       <div className="flex min-w-0 flex-1 flex-col">
//         <InspectorTopbar
//           onOpenMenu={() => setMenuOpen(true)}
//           name={user.name}
//           role={user.role}
//           imageUrl={user.imageUrl}
//         />
//         {children}
//       </div>

//       <MobileBottomNav />
//     </div>
//   );
// }


// "use client";

// import { useState } from "react";
// import InspectorSidebar from "./InspectorSidebar";
// import MobileDrawer from "./MobileDrawer";
// import MobileBottomNav from "./MobileBottomNav";
// import InspectorTopbar from "./InspectorTopbar";

// type InspectorUser = {
//   name: string;
//   email: string;
//   role: string;
//   imageUrl: string | null;
// };

// export default function InspectorShell({
//   user,
//   children,
// }: {
//   user: InspectorUser;
//   children: React.ReactNode;
// }) {
//   const [menuOpen, setMenuOpen] = useState(false);

//   return (
//     <div className="flex min-h-screen bg-[#F7FAFC]">
//       {/* Desktop sidebar — sticky, does NOT scroll with page */}
//       <InspectorSidebar />

//       {/* Mobile slide-in drawer */}
//       <MobileDrawer open={menuOpen} onClose={() => setMenuOpen(false)} />

//       {/* Main column */}
//       <div className="flex min-w-0 flex-1 flex-col">
//         <InspectorTopbar
//           onOpenMenu={() => setMenuOpen(true)}
//           name={user.name}
//           role={user.role}
//           imageUrl={user.imageUrl}
//         />
//         {children}
//       </div>

//       {/* Mobile bottom navigation */}
//       <MobileBottomNav />
//     </div>
//   );
// }



"use client";

import { useState } from "react";
import InspectorSidebar from "./InspectorSidebar";
import MobileDrawer from "./MobileDrawer";
import MobileBottomNav from "./MobileBottomNav";
import InspectorTopbar from "./InspectorTopbar";

type InspectorUser = {
  name: string;
  email: string;
  role: string;
  imageUrl: string | null;
};

export default function InspectorShell({
  user,
  children,
}: {
  user: InspectorUser;
  children: React.ReactNode;
}) {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <div className="flex min-h-screen bg-[#F7FAFC]">
      {/* Desktop sidebar — sticky, does NOT scroll with page */}
      <InspectorSidebar />

      {/* Mobile slide-in drawer */}
      <MobileDrawer open={menuOpen} onClose={() => setMenuOpen(false)} />

      {/* Main column */}
      <div className="flex min-w-0 flex-1 flex-col">
        <InspectorTopbar
          onOpenMenu={() => setMenuOpen(true)}
          name={user.name}
          role={user.role}
          imageUrl={user.imageUrl}
        />

        {/* Page container — consistent width + padding for ALL pages */}
        <main className="flex-1 px-4 py-6 pb-24 sm:px-6 lg:px-8 lg:pb-6">
          <div className="mx-auto w-full max-w-[1400px]">{children}</div>
        </main>
      </div>

      {/* Mobile bottom navigation */}
      <MobileBottomNav />
    </div>
  );
}