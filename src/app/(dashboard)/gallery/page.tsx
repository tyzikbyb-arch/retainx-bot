import { Video, Image as ImageIcon, Mic, Heart, Download } from "lucide-react";

const ITEMS = [
  { type: "video", model: "Kling 2.0", prompt: "Cyberpunk city at night, rain reflections on streets, neon lights", user: "alex_m", likes: 142, gradient: "linear-gradient(135deg,#1a0533 0%,#0d1a33 100%)" },
  { type: "image", model: "Grok Aurora", prompt: "Abstract golden waves on deep space background, ultra detailed", user: "studio_x", likes: 89, gradient: "linear-gradient(135deg,#1a0f00 0%,#2d1800 100%)" },
  { type: "video", model: "Sora", prompt: "Aerial cinematic shot of mountain peaks at sunrise, epic clouds", user: "creator99", likes: 234, gradient: "linear-gradient(135deg,#001a33 0%,#001122 100%)" },
  { type: "audio", model: "ElevenLabs", prompt: "Documentary narrator: calm, authoritative, British accent", user: "voice_pro", likes: 56, gradient: "linear-gradient(135deg,#001a0d 0%,#002211 100%)" },
  { type: "video", model: "MiniMax", prompt: "Slow motion water droplets, macro lens, dark background, 4K", user: "nature_lens", likes: 178, gradient: "linear-gradient(135deg,#0d0033 0%,#1a0033 100%)" },
  { type: "image", model: "Flux Pro", prompt: "Portrait of a futuristic warrior, dramatic rim light, dark fantasy", user: "art_ai", likes: 321, gradient: "linear-gradient(135deg,#1a1a00 0%,#0d2200 100%)" },
  { type: "video", model: "WAN 2.1", prompt: "Time-lapse of blooming flowers in ultra slow motion", user: "bloom_studio", likes: 95, gradient: "linear-gradient(135deg,#001a1a 0%,#002222 100%)" },
  { type: "image", model: "Grok Aurora", prompt: "Neon geometric shapes, dark background, synthwave aesthetic", user: "neon_art", likes: 267, gradient: "linear-gradient(135deg,#1a0033 0%,#002233 100%)" },
  { type: "video", model: "LTX Video", prompt: "Product reveal animation: sleek smartwatch floating in dark space", user: "brand_x", likes: 143, gradient: "linear-gradient(135deg,#001122 0%,#110022 100%)" },
];

const typeColor: Record<string, string> = { video: "#7c3aed", image: "#f59e0b", audio: "#06b6d4" };
const TypeIcon = ({ t }: { t: string }) => t === "video" ? <Video size={13} /> : t === "image" ? <ImageIcon size={13} /> : <Mic size={13} />;

export default function GalleryPage() {
  return (
    <div className="p-8">
      <div className="mb-8 flex items-center justify-between flex-wrap gap-4">
        <div><h1 className="text-3xl font-black mb-1">Community Gallery</h1><p style={{ color: "var(--text-secondary)" }}>Discover what others are creating. All prompts are public.</p></div>
        <div className="flex gap-2">
          {["All", "Video", "Image", "Audio"].map((t) => (<button key={t} className="px-4 py-2 rounded-xl text-sm font-medium transition-all" style={t === "All" ? { background: "var(--accent)", color: "#fff", border: "none", cursor: "pointer" } : { background: "var(--bg-card)", color: "var(--text-secondary)", border: "1px solid var(--border)", cursor: "pointer" }}>{t}</button>))}
        </div>
      </div>
      <div className="columns-1 sm:columns-2 md:columns-3 gap-4 space-y-4">
        {ITEMS.map((item, i) => (
          <div key={i} className="break-inside-avoid rounded-2xl overflow-hidden group cursor-pointer" style={{ border: "1px solid var(--border)" }}>
            <div className="w-full relative" style={{ height: i % 3 === 0 ? 200 : i % 3 === 1 ? 160 : 240, background: item.gradient }}>
              <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-3" style={{ background: "rgba(0,0,0,0.6)" }}>
                <button className="w-10 h-10 rounded-full flex items-center justify-center transition-all hover:scale-110" style={{ background: "rgba(255,255,255,0.15)", border: "1px solid rgba(255,255,255,0.3)", cursor: "pointer" }}><Heart size={16} color="#fff" /></button>
                <button className="w-10 h-10 rounded-full flex items-center justify-center transition-all hover:scale-110" style={{ background: "rgba(255,255,255,0.15)", border: "1px solid rgba(255,255,255,0.3)", cursor: "pointer" }}><Download size={16} color="#fff" /></button>
              </div>
            </div>
            <div className="p-4" style={{ background: "var(--bg-card)" }}>
              <div className="flex items-center gap-2 mb-2">
                <div className="flex items-center gap-1 text-[10px] font-bold px-2 py-0.5 rounded" style={{ background: (typeColor[item.type] || "#7c3aed") + "22", color: typeColor[item.type] || "#7c3aed" }}><TypeIcon t={item.type} />{item.type.toUpperCase()}</div>
                <span className="text-[10px]" style={{ color: "var(--text-muted)" }}>{item.model}</span>
              </div>
              <p className="text-sm leading-snug mb-3 line-clamp-2" style={{ color: "var(--text-secondary)" }}>{item.prompt}</p>
              <div className="flex items-center justify-between">
                <span className="text-xs font-medium" style={{ color: "var(--text-muted)" }}>@{item.user}</span>
                <div className="flex items-center gap-1 text-xs" style={{ color: "var(--text-muted)" }}><Heart size={11} />{item.likes}</div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
