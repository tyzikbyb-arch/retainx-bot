import Link from "next/link";
import { Video, Image as ImageIcon, Mic, ArrowRight, TrendingUp, Clock, Zap } from "lucide-react";

const QUICK_ACTIONS = [
  { href: "/generate/video", icon: Video, label: "Generate Video", desc: "Sora, Kling, WAN and 4 more", color: "#7c3aed" },
  { href: "/generate/image", icon: ImageIcon, label: "Generate Image", desc: "Grok Aurora, Flux Pro, SDXL", color: "#f59e0b" },
  { href: "/generate/audio", icon: Mic, label: "Generate Audio", desc: "ElevenLabs, Cartesia voices", color: "#06b6d4" },
];

const RECENT = [
  { type: "video", model: "Kling 2.0", prompt: "Cyberpunk city at night, rain and neon lights", credits: 6, ago: "2h ago" },
  { type: "image", model: "Grok Aurora", prompt: "Abstract golden waves on dark background", credits: 1, ago: "5h ago" },
  { type: "video", model: "WAN 2.1", prompt: "Ocean waves crashing on rocky shore, slow motion", credits: 4, ago: "1d ago" },
  { type: "audio", model: "ElevenLabs", prompt: "Professional male narrator voice, calm and clear", credits: 2, ago: "2d ago" },
];

const typeColor: Record<string, string> = { video: "#7c3aed", image: "#f59e0b", audio: "#06b6d4" };

export default function DashboardPage() {
  return (
    <div className="p-8 max-w-5xl">
      <div className="mb-8">
        <h1 className="text-3xl font-black mb-1">Good morning 👋</h1>
        <p style={{ color: "var(--text-secondary)" }}>What are you creating today?</p>
      </div>
      <div className="grid grid-cols-3 gap-4 mb-8">
        {[{ icon: Zap, label: "Credits left", value: "42", sub: "≈ $2.10" }, { icon: TrendingUp, label: "Generations", value: "18", sub: "this month" }, { icon: Clock, label: "Avg. wait time", value: "~4 min", sub: "for video" }].map(({ icon: Icon, label, value, sub }) => (
          <div key={label} className="rounded-2xl p-5" style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}>
            <div className="flex items-center gap-2 mb-3"><Icon size={16} style={{ color: "var(--accent-bright)" }} /><span className="text-xs font-medium" style={{ color: "var(--text-muted)" }}>{label}</span></div>
            <div className="text-2xl font-black mb-0.5">{value}</div>
            <div className="text-xs" style={{ color: "var(--text-muted)" }}>{sub}</div>
          </div>
        ))}
      </div>
      <h2 className="text-lg font-bold mb-4">Quick Start</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-10">
        {QUICK_ACTIONS.map(({ href, icon: Icon, label, desc, color }) => (
          <Link key={href} href={href} className="group rounded-2xl p-6 flex flex-col gap-4 transition-all" style={{ background: "var(--bg-card)", border: "1px solid var(--border)", textDecoration: "none" }}>
            <div className="w-12 h-12 rounded-xl flex items-center justify-center" style={{ background: color + "22", color }}><Icon size={22} /></div>
            <div><div className="font-bold mb-1 group-hover:text-white transition-colors">{label}</div><div className="text-sm" style={{ color: "var(--text-muted)" }}>{desc}</div></div>
            <div className="flex items-center gap-1 text-sm font-medium" style={{ color }}>Create <ArrowRight size={14} /></div>
          </Link>
        ))}
      </div>
      <h2 className="text-lg font-bold mb-4">Recent Generations</h2>
      <div className="rounded-2xl overflow-hidden" style={{ border: "1px solid var(--border)", background: "var(--bg-card)" }}>
        {RECENT.map((r, i) => (
          <div key={i} className="flex items-center gap-4 px-6 py-4" style={{ borderBottom: i < RECENT.length - 1 ? "1px solid var(--border)" : "none" }}>
            <div className="w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0" style={{ background: typeColor[r.type] + "22", color: typeColor[r.type] }}>
              {r.type === "video" ? <Video size={16} /> : r.type === "image" ? <ImageIcon size={16} /> : <Mic size={16} />}
            </div>
            <div className="flex-1 min-w-0"><div className="text-sm font-medium truncate">{r.prompt}</div><div className="text-xs mt-0.5" style={{ color: "var(--text-muted)" }}>{r.model}</div></div>
            <div className="text-xs" style={{ color: "var(--text-muted)" }}>{r.credits} cr</div>
            <div className="text-xs" style={{ color: "var(--text-muted)" }}>{r.ago}</div>
            <div className="text-xs font-medium px-2.5 py-1 rounded-full" style={{ background: "rgba(34,197,94,0.12)", color: "#22c55e" }}>Done</div>
          </div>
        ))}
        <div className="px-6 py-4" style={{ borderTop: "1px solid var(--border)" }}>
          <Link href="/history" className="text-sm font-medium flex items-center gap-1" style={{ color: "var(--accent-bright)", textDecoration: "none" }}>View all history <ArrowRight size={14} /></Link>
        </div>
      </div>
    </div>
  );
}
