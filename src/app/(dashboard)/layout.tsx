"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { LayoutDashboard, Video, Image as ImageIcon, Mic, Images, History, CreditCard, LogOut, ChevronRight, Zap } from "lucide-react";

const NAV = [
  { href: "/dashboard", icon: LayoutDashboard, label: "Dashboard" },
  { href: "/generate/video", icon: Video, label: "Video" },
  { href: "/generate/image", icon: ImageIcon, label: "Image" },
  { href: "/generate/audio", icon: Mic, label: "Audio" },
  { href: "/gallery", icon: Images, label: "Gallery" },
  { href: "/history", icon: History, label: "History" },
  { href: "/billing", icon: CreditCard, label: "Billing" },
];

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const path = usePathname();
  return (
    <div className="flex min-h-screen" style={{ background: "var(--bg)" }}>
      <aside className="w-60 flex flex-col fixed left-0 top-0 bottom-0 z-40" style={{ background: "var(--bg-surface)", borderRight: "1px solid var(--border)" }}>
        <div className="px-5 py-5" style={{ borderBottom: "1px solid var(--border)" }}>
          <Link href="/" className="flex items-center gap-2 font-bold" style={{ textDecoration: "none" }}>
            <div className="w-8 h-8 rounded-lg flex items-center justify-center text-white font-black text-sm" style={{ background: "linear-gradient(135deg,#7c3aed,#06b6d4)" }}>R</div>
            <span style={{ background: "linear-gradient(135deg,#a78bfa,#06b6d4)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>RetainX</span>
          </Link>
        </div>
        <div className="mx-3 mt-4 mb-2 rounded-xl p-4" style={{ background: "var(--accent-dim)", border: "1px solid var(--accent)" }}>
          <div className="flex items-center justify-between mb-1">
            <span className="text-xs font-medium" style={{ color: "var(--accent-bright)" }}>Credits</span>
            <Zap size={14} style={{ color: "var(--accent-bright)" }} />
          </div>
          <div className="text-2xl font-black mb-1">42</div>
          <div className="text-xs mb-3" style={{ color: "var(--text-muted)" }}>≈ $2.10 remaining</div>
          <Link href="/billing" className="text-xs font-semibold flex items-center gap-1" style={{ color: "var(--accent-bright)", textDecoration: "none" }}>Top up <ChevronRight size={12} /></Link>
        </div>
        <nav className="flex-1 px-3 py-2 overflow-y-auto">
          {NAV.map(({ href, icon: Icon, label }) => {
            const active = path === href || (href !== "/dashboard" && path.startsWith(href));
            return (
              <Link key={href} href={href} className="flex items-center gap-3 px-3 py-2.5 rounded-xl mb-1 text-sm font-medium transition-all" style={{ textDecoration: "none", background: active ? "var(--accent-dim)" : "transparent", color: active ? "var(--accent-bright)" : "var(--text-secondary)", borderLeft: active ? "2px solid var(--accent)" : "2px solid transparent" }}>
                <Icon size={17} />{label}
              </Link>
            );
          })}
        </nav>
        <div className="px-3 py-4" style={{ borderTop: "1px solid var(--border)" }}>
          <div className="flex items-center gap-3 px-3 py-2 rounded-xl" style={{ background: "var(--bg-card)" }}>
            <div className="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold text-white" style={{ background: "linear-gradient(135deg,#7c3aed,#06b6d4)" }}>U</div>
            <div className="flex-1 min-w-0">
              <div className="text-sm font-medium truncate">User</div>
              <div className="text-xs truncate" style={{ color: "var(--text-muted)" }}>user@example.com</div>
            </div>
            <button style={{ background: "none", border: "none", cursor: "pointer", color: "var(--text-muted)" }}><LogOut size={15} /></button>
          </div>
        </div>
      </aside>
      <main className="flex-1 ml-60 min-h-screen">{children}</main>
    </div>
  );
}
