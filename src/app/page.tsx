import Link from "next/link";
import {
  Video,
  Image as ImageIcon,
  Mic,
  Zap,
  ArrowRight,
  Check,
  Layers,
  Globe,
  Shield,
  ChevronRight,
} from "lucide-react";

const MODELS = [
  { name: "Sora", type: "Video", price: "$0.50", badge: "OpenAI", color: "#7c3aed" },
  { name: "Kling 2.0", type: "Video", price: "$0.30", badge: "Popular", color: "#06b6d4" },
  { name: "Seedance", type: "Video", price: "$0.25", badge: "Fast", color: "#f59e0b" },
  { name: "WAN 2.1", type: "Video", price: "$0.20", badge: "Quality", color: "#22c55e" },
  { name: "LTX Video", type: "Video", price: "$0.15", badge: "Budget", color: "#ec4899" },
  { name: "MiniMax", type: "Video", price: "$0.25", badge: "Cinematic", color: "#8b5cf6" },
  { name: "Grok Aurora", type: "Image", price: "$0.05", badge: "xAI", color: "#06b6d4" },
  { name: "HeyGen", type: "Video", price: "$0.50", badge: "Avatar", color: "#f97316" },
  { name: "ElevenLabs", type: "Audio", price: "$0.10", badge: "Voice", color: "#a78bfa" },
];

const FEATURES = [
  { icon: Layers, title: "15+ AI Models", desc: "Sora, Kling, WAN, LTX, Seedance, MiniMax, HeyGen, ElevenLabs — all in one place." },
  { icon: Zap, title: "No Subscriptions", desc: "Pay only for what you generate. 1 credit = $0.05. Top up any amount, use forever." },
  { icon: Globe, title: "Compare All Models", desc: "Run the same prompt across multiple models simultaneously. Choose what's best for your project." },
  { icon: Shield, title: "Your Creations, Your Rights", desc: "Full commercial rights on everything you generate. No platform watermarks." },
];

const PRICING = [
  { cat: "Video Generation", items: [
    { name: "Sora (OpenAI)", credits: 10, usd: "$0.50" },
    { name: "Kling 2.0", credits: 6, usd: "$0.30" },
    { name: "Seedance", credits: 5, usd: "$0.25" },
    { name: "WAN 2.1", credits: 4, usd: "$0.20" },
    { name: "LTX Video", credits: 3, usd: "$0.15" },
    { name: "MiniMax Video", credits: 5, usd: "$0.25" },
    { name: "HeyGen Avatar", credits: 10, usd: "$0.50" },
  ]},
  { cat: "Image Generation", items: [
    { name: "Grok Aurora", credits: 1, usd: "$0.05" },
    { name: "Stable Diffusion XL", credits: 1, usd: "$0.05" },
    { name: "Flux Pro", credits: 2, usd: "$0.10" },
  ]},
  { cat: "Audio / Voice", items: [
    { name: "ElevenLabs", credits: 2, usd: "$0.10" },
    { name: "Cartesia", credits: 2, usd: "$0.10" },
  ]},
];

const GALLERY_ITEMS = [
  { prompt: "Cyberpunk city at night, rain reflections, cinematic", model: "Kling 2.0", type: "video", gradient: "linear-gradient(135deg,#1a0533,#0d1a33)" },
  { prompt: "Golden hour over mountain peaks, aerial view", model: "Sora", type: "video", gradient: "linear-gradient(135deg,#1a0f00,#332200)" },
  { prompt: "Abstract fluid art, deep purple and gold", model: "Grok Aurora", type: "image", gradient: "linear-gradient(135deg,#1a0033,#330011)" },
  { prompt: "Futuristic product launch animation", model: "LTX Video", type: "video", gradient: "linear-gradient(135deg,#001a2e,#002233)" },
  { prompt: "Portrait of a warrior, dramatic lighting", model: "Grok Aurora", type: "image", gradient: "linear-gradient(135deg,#1a1a00,#0d2200)" },
  { prompt: "Ocean waves crashing, slow motion", model: "WAN 2.1", type: "video", gradient: "linear-gradient(135deg,#001a33,#001122)" },
  { prompt: "Neon logo reveal animation", model: "MiniMax", type: "video", gradient: "linear-gradient(135deg,#0d0033,#1a0033)" },
  { prompt: "Professional voice narration — travel documentary", model: "ElevenLabs", type: "audio", gradient: "linear-gradient(135deg,#001a0d,#002211)" },
];

function Orb({ style }: { style: React.CSSProperties }) {
  return <div className="absolute rounded-full pointer-events-none animate-pulse-glow" style={{ filter: "blur(80px)", ...style }} />;
}

function ModelBadge({ model }: { model: typeof MODELS[0] }) {
  return (
    <div className="card-glow flex items-center gap-3 rounded-xl px-4 py-3 cursor-default" style={{ background: "var(--bg-card)" }}>
      <div className="w-8 h-8 rounded-lg flex items-center justify-center text-xs font-bold text-white" style={{ background: model.color + "33", border: `1px solid ${model.color}55` }}>
        {model.name[0]}
      </div>
      <div className="flex-1 min-w-0">
        <div className="text-sm font-medium text-[var(--text-primary)] truncate">{model.name}</div>
        <div className="text-xs text-[var(--text-muted)]">{model.type}</div>
      </div>
      <div className="text-sm font-semibold" style={{ color: model.color }}>{model.price}</div>
    </div>
  );
}

function GalleryCard({ item }: { item: typeof GALLERY_ITEMS[0] }) {
  const typeColor = item.type === "video" ? "#7c3aed" : item.type === "audio" ? "#06b6d4" : "#f59e0b";
  return (
    <div className="flex-shrink-0 w-56 h-40 rounded-2xl overflow-hidden relative cursor-pointer group" style={{ border: "1px solid var(--border)" }}>
      <div className="absolute inset-0" style={{ background: item.gradient }} />
      <div className="absolute inset-0 flex flex-col justify-end p-3 bg-gradient-to-t from-black/80 via-transparent to-transparent">
        <div className="text-[10px] font-semibold uppercase tracking-wider mb-1 px-2 py-0.5 rounded-full w-fit" style={{ background: typeColor + "22", color: typeColor, border: `1px solid ${typeColor}44` }}>
          {item.type}
        </div>
        <p className="text-white text-xs font-medium line-clamp-2 leading-tight">{item.prompt}</p>
        <p className="text-[10px] mt-1" style={{ color: "var(--text-muted)" }}>{item.model}</p>
      </div>
      <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity" style={{ background: "var(--accent-dim)" }} />
    </div>
  );
}

export default function LandingPage() {
  return (
    <div style={{ background: "var(--bg)", color: "var(--text-primary)", minHeight: "100vh" }}>
      <nav className="fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-6 py-4" style={{ borderBottom: "1px solid var(--border)", background: "rgba(2,2,8,0.85)", backdropFilter: "blur(20px)" }}>
        <Link href="/" className="flex items-center gap-2 font-bold text-lg">
          <div className="w-8 h-8 rounded-lg flex items-center justify-center text-white font-black text-sm" style={{ background: "linear-gradient(135deg,#7c3aed,#06b6d4)" }}>R</div>
          <span className="gradient-text">RetainX</span>
          <span style={{ color: "var(--text-secondary)", fontWeight: 400 }}>Studio</span>
        </Link>
        <div className="hidden md:flex items-center gap-8 text-sm" style={{ color: "var(--text-secondary)" }}>
          <Link href="#models" className="hover:text-white transition-colors">Models</Link>
          <Link href="#features" className="hover:text-white transition-colors">Features</Link>
          <Link href="#pricing" className="hover:text-white transition-colors">Pricing</Link>
          <Link href="#gallery" className="hover:text-white transition-colors">Gallery</Link>
        </div>
        <div className="flex items-center gap-3">
          <Link href="/login" className="btn-ghost text-sm px-4 py-2 hidden md:block" style={{ textDecoration: "none" }}>Sign in</Link>
          <Link href="/register" className="btn-primary text-sm px-5 py-2" style={{ textDecoration: "none", borderRadius: "10px" }}>Get Started Free</Link>
        </div>
      </nav>

      <section className="relative min-h-screen flex flex-col items-center justify-center px-6 text-center pt-20 overflow-hidden">
        <Orb style={{ width: 600, height: 600, top: "10%", left: "50%", transform: "translateX(-50%)", background: "var(--accent)", opacity: 0.12 }} />
        <Orb style={{ width: 400, height: 400, top: "20%", left: "10%", background: "#06b6d4", opacity: 0.08 }} />
        <Orb style={{ width: 300, height: 300, bottom: "20%", right: "10%", background: "#7c3aed", opacity: 0.1 }} />
        <div className="absolute inset-0 pointer-events-none" style={{ backgroundImage: "linear-gradient(var(--border) 1px, transparent 1px), linear-gradient(90deg, var(--border) 1px, transparent 1px)", backgroundSize: "64px 64px", opacity: 0.3 }} />
        <div className="relative z-10 max-w-5xl mx-auto">
          <div className="inline-flex items-center gap-2 rounded-full px-4 py-2 text-sm font-medium mb-8" style={{ background: "var(--accent-dim)", border: "1px solid var(--accent)", color: "var(--accent-bright)" }}>
            <div className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse" />
            15+ AI Models Available Now
          </div>
          <h1 className="text-5xl md:text-7xl font-black leading-none tracking-tight mb-6" style={{ letterSpacing: "-0.03em" }}>
            Every AI Model.<br /><span className="gradient-text">One Platform.</span>
          </h1>
          <p className="text-xl md:text-2xl max-w-2xl mx-auto mb-4" style={{ color: "var(--text-secondary)" }}>Generate videos, images, and audio with Sora, Kling, WAN, LTX, HeyGen and 10 more.</p>
          <p className="text-lg font-semibold mb-10" style={{ color: "var(--accent-bright)" }}>No subscriptions. No monthly fees. Pay per creation.</p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
            <Link href="/register" className="btn-primary flex items-center gap-2 px-8 py-4 text-lg" style={{ textDecoration: "none", borderRadius: "14px" }}>Start Creating Free <ArrowRight size={20} /></Link>
            <Link href="#gallery" className="btn-ghost flex items-center gap-2 px-8 py-4 text-lg" style={{ textDecoration: "none" }}>See Examples</Link>
          </div>
          <div className="flex flex-wrap items-center justify-center gap-8 text-sm" style={{ color: "var(--text-muted)" }}>
            {[{ v: "15+", l: "AI Models" }, { v: "$0.05", l: "Per credit" }, { v: "3", l: "Content types" }, { v: "100%", l: "Your rights" }].map(({ v, l }) => (
              <div key={l} className="flex flex-col items-center gap-1">
                <span className="text-2xl font-black" style={{ color: "var(--text-primary)" }}>{v}</span>
                <span>{l}</span>
              </div>
            ))}
          </div>
        </div>
        <div className="absolute bottom-0 left-0 right-0 h-32 pointer-events-none" style={{ background: "linear-gradient(to top, var(--bg), transparent)" }} />
      </section>

      <section id="models" className="py-24 px-6 max-w-7xl mx-auto">
        <div className="text-center mb-14">
          <p className="text-sm font-semibold uppercase tracking-widest mb-3" style={{ color: "var(--accent-bright)" }}>Model Library</p>
          <h2 className="text-4xl font-black tracking-tight mb-4">Every top model, zero switching</h2>
          <p className="text-lg max-w-xl mx-auto" style={{ color: "var(--text-secondary)" }}>Run your prompt on one model or all of them. See the difference. Choose the winner.</p>
        </div>
        <div className="flex flex-wrap justify-center gap-2 mb-10">
          {["All", "Video", "Image", "Audio"].map((t) => (
            <div key={t} className="px-5 py-2 rounded-full text-sm font-medium cursor-pointer transition-all" style={t === "All" ? { background: "var(--accent)", color: "#fff" } : { background: "var(--bg-card)", color: "var(--text-secondary)", border: "1px solid var(--border)" }}>{t}</div>
          ))}
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
          {MODELS.map((m) => <ModelBadge key={m.name} model={m} />)}
        </div>
        <div className="mt-12 rounded-2xl p-8 text-center" style={{ background: "linear-gradient(135deg, var(--bg-card) 0%, var(--bg-surface) 100%)", border: "1px solid var(--border)" }}>
          <h3 className="text-2xl font-bold mb-3">Can&apos;t decide which model?</h3>
          <p className="mb-6" style={{ color: "var(--text-secondary)" }}>Use our <strong style={{ color: "var(--accent-bright)" }}>Multi-Model Comparison</strong> — generate one prompt on 3 models side-by-side and pick the best result.</p>
          <Link href="/register" className="btn-primary inline-flex items-center gap-2 px-6 py-3" style={{ textDecoration: "none", borderRadius: "10px" }}>Try Comparison Mode <ChevronRight size={16} /></Link>
        </div>
      </section>

      <section id="features" className="py-24 px-6" style={{ background: "var(--bg-surface)" }}>
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-14">
            <p className="text-sm font-semibold uppercase tracking-widest mb-3" style={{ color: "var(--accent-bright)" }}>Why RetainX</p>
            <h2 className="text-4xl font-black tracking-tight mb-4">Built different</h2>
            <p className="text-lg max-w-xl mx-auto" style={{ color: "var(--text-secondary)" }}>While others lock you into subscriptions and single models, we give you the entire market.</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {FEATURES.map((f) => (
              <div key={f.title} className="card-glow rounded-2xl p-8 flex gap-5" style={{ background: "var(--bg-card)" }}>
                <div className="w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0" style={{ background: "var(--accent-dim)", color: "var(--accent-bright)" }}><f.icon size={22} /></div>
                <div><h3 className="text-xl font-bold mb-2">{f.title}</h3><p style={{ color: "var(--text-secondary)", lineHeight: 1.7 }}>{f.desc}</p></div>
              </div>
            ))}
          </div>
          <div className="mt-16 rounded-2xl overflow-hidden" style={{ border: "1px solid var(--border)" }}>
            <div className="px-8 py-5" style={{ background: "var(--bg-card)" }}><h3 className="text-xl font-bold">RetainX vs. the rest</h3></div>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr style={{ borderBottom: "1px solid var(--border)", background: "var(--bg-surface)" }}>
                    <th className="text-left px-8 py-4 font-medium" style={{ color: "var(--text-muted)" }}>Feature</th>
                    <th className="px-6 py-4 font-bold" style={{ color: "var(--accent-bright)" }}>RetainX</th>
                    <th className="px-6 py-4 font-medium" style={{ color: "var(--text-muted)" }}>Runway</th>
                    <th className="px-6 py-4 font-medium" style={{ color: "var(--text-muted)" }}>Pika</th>
                    <th className="px-6 py-4 font-medium" style={{ color: "var(--text-muted)" }}>Leonardo</th>
                  </tr>
                </thead>
                <tbody>
                  {[
                    ["15+ AI models", true, false, false, false],
                    ["No subscription required", true, false, false, false],
                    ["Pay per generation", true, false, false, "partial"],
                    ["Multi-model comparison", true, false, false, false],
                    ["Video + Audio bundles", true, false, false, false],
                    ["Price shown before generating", true, false, false, false],
                    ["Commercial rights", true, true, true, true],
                  ].map(([label, rx, rw, pk, lx]) => (
                    <tr key={label as string} style={{ borderBottom: "1px solid var(--border)" }}>
                      <td className="px-8 py-4" style={{ color: "var(--text-secondary)" }}>{label}</td>
                      {[rx, rw, pk, lx].map((v, i) => (
                        <td key={i} className="px-6 py-4 text-center">
                          {v === true ? <Check size={18} className="inline" style={{ color: "var(--green)" }} /> : v === "partial" ? <span className="text-xs" style={{ color: "var(--gold)" }}>Partial</span> : <span style={{ color: "var(--text-muted)" }}>–</span>}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </section>

      <section id="pricing" className="py-24 px-6 max-w-7xl mx-auto">
        <div className="text-center mb-14">
          <p className="text-sm font-semibold uppercase tracking-widest mb-3" style={{ color: "var(--accent-bright)" }}>Pricing</p>
          <h2 className="text-4xl font-black tracking-tight mb-4">No surprises. Ever.</h2>
          <p className="text-lg max-w-xl mx-auto" style={{ color: "var(--text-secondary)" }}>Every price shown upfront. 1 credit = $0.05. Buy once, use whenever.</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {PRICING.map((cat) => (
            <div key={cat.cat} className="card-glow rounded-2xl overflow-hidden" style={{ background: "var(--bg-card)" }}>
              <div className="px-6 py-4 flex items-center gap-3" style={{ borderBottom: "1px solid var(--border)" }}>
                {cat.cat.includes("Video") ? <Video size={18} style={{ color: "var(--accent-bright)" }} /> : cat.cat.includes("Image") ? <ImageIcon size={18} style={{ color: "var(--gold)" }} /> : <Mic size={18} style={{ color: "var(--cyan)" }} />}
                <span className="font-bold">{cat.cat}</span>
              </div>
              <div className="p-4 flex flex-col gap-2">
                {cat.items.map((item) => (
                  <div key={item.name} className="flex items-center justify-between px-4 py-3 rounded-xl" style={{ background: "var(--bg-surface)" }}>
                    <span className="text-sm" style={{ color: "var(--text-secondary)" }}>{item.name}</span>
                    <div className="flex items-center gap-3">
                      <span className="text-xs" style={{ color: "var(--text-muted)" }}>{item.credits} cr</span>
                      <span className="text-sm font-bold" style={{ color: "var(--text-primary)" }}>{item.usd}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
        <div className="mt-12 text-center">
          <h3 className="text-2xl font-bold mb-8">Top up your credits</h3>
          <div className="flex flex-wrap justify-center gap-4">
            {[{ credits: 20, usd: "$1.00", tag: "" }, { credits: 100, usd: "$5.00", tag: "Popular" }, { credits: 200, usd: "$10.00", tag: "" }, { credits: 500, usd: "$25.00", tag: "Best Value" }].map((pack) => (
              <Link key={pack.credits} href="/register" className="card-glow rounded-2xl p-6 text-center relative w-44 cursor-pointer no-underline" style={{ background: "var(--bg-card)", textDecoration: "none" }}>
                {pack.tag && <div className="absolute -top-3 left-1/2 -translate-x-1/2 text-xs font-bold px-3 py-1 rounded-full" style={{ background: "var(--accent)", color: "#fff" }}>{pack.tag}</div>}
                <div className="text-3xl font-black mb-1" style={{ color: "var(--accent-bright)" }}>{pack.credits}</div>
                <div className="text-xs mb-3" style={{ color: "var(--text-muted)" }}>credits</div>
                <div className="text-xl font-bold">{pack.usd}</div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      <section id="gallery" className="py-24 overflow-hidden" style={{ background: "var(--bg-surface)" }}>
        <div className="text-center mb-12 px-6">
          <p className="text-sm font-semibold uppercase tracking-widest mb-3" style={{ color: "var(--accent-bright)" }}>Community Gallery</p>
          <h2 className="text-4xl font-black tracking-tight mb-4">Created by real users</h2>
          <p className="text-lg" style={{ color: "var(--text-secondary)" }}>All prompts are public. Remix, get inspired, go further.</p>
        </div>
        <div className="flex gap-4 mb-4 w-full overflow-hidden">
          <div className="flex gap-4 animate-scroll-left">
            {[...GALLERY_ITEMS, ...GALLERY_ITEMS].map((item, i) => <GalleryCard key={i} item={item} />)}
          </div>
        </div>
        <div className="flex gap-4 w-full overflow-hidden" style={{ direction: "rtl" }}>
          <div className="flex gap-4 animate-scroll-left" style={{ direction: "ltr" }}>
            {[...GALLERY_ITEMS.slice(4), ...GALLERY_ITEMS.slice(0, 4), ...GALLERY_ITEMS.slice(4), ...GALLERY_ITEMS.slice(0, 4)].map((item, i) => <GalleryCard key={i} item={item} />)}
          </div>
        </div>
      </section>

      <section className="py-32 px-6 text-center relative overflow-hidden">
        <Orb style={{ width: 500, height: 500, top: "50%", left: "50%", transform: "translate(-50%,-50%)", background: "var(--accent)", opacity: 0.1 }} />
        <div className="relative z-10 max-w-3xl mx-auto">
          <h2 className="text-5xl md:text-6xl font-black tracking-tight mb-6">Ready to create?</h2>
          <p className="text-xl mb-10" style={{ color: "var(--text-secondary)" }}>Join thousands of creators generating with RetainX Studio. Start free — no credit card required.</p>
          <Link href="/register" className="btn-primary inline-flex items-center gap-3 px-10 py-5 text-xl" style={{ textDecoration: "none", borderRadius: "16px" }}>Start Creating Free <ArrowRight size={24} /></Link>
          <p className="mt-6 text-sm" style={{ color: "var(--text-muted)" }}>Also available on Telegram → <strong style={{ color: "var(--accent-bright)" }}>@RetainXStudioBot</strong></p>
        </div>
      </section>

      <footer className="px-6 py-12" style={{ borderTop: "1px solid var(--border)", background: "var(--bg-surface)" }}>
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-2 font-bold">
            <div className="w-7 h-7 rounded-lg flex items-center justify-center text-white text-xs font-black" style={{ background: "linear-gradient(135deg,#7c3aed,#06b6d4)" }}>R</div>
            <span className="gradient-text">RetainX Studio</span>
          </div>
          <div className="flex gap-6 text-sm" style={{ color: "var(--text-muted)" }}>
            <Link href="/login" className="hover:text-white transition-colors" style={{ textDecoration: "none" }}>Sign In</Link>
            <Link href="/register" className="hover:text-white transition-colors" style={{ textDecoration: "none" }}>Get Started</Link>
            <span>© 2025 RetainX Studio</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
