"use client";

import { useState } from "react";
import { Zap, Image as ImageIcon } from "lucide-react";

const IMAGE_MODELS = [
  { id: "grok", name: "Grok Aurora", provider: "xAI", credits: 1, usd: "$0.05", speed: "~30s", badge: "Popular" },
  { id: "flux", name: "Flux Pro 1.1", provider: "Black Forest Labs", credits: 2, usd: "$0.10", speed: "~45s", badge: "High Quality" },
  { id: "sdxl", name: "Stable Diffusion XL", provider: "Stability AI", credits: 1, usd: "$0.05", speed: "~20s", badge: "Fast" },
];

const STYLES = ["Photorealistic", "Cinematic", "Anime", "Digital Art", "Oil Painting", "Minimalist", "Dark Fantasy"];
const SIZES = ["512×512", "768×768", "1024×1024", "1024×1792", "1792×1024"];

export default function ImageGeneratePage() {
  const [prompt, setPrompt] = useState("");
  const [model, setModel] = useState("grok");
  const [style, setStyle] = useState("Photorealistic");
  const [size, setSize] = useState("1024×1024");
  const [loading, setLoading] = useState(false);

  const active = IMAGE_MODELS.find((m) => m.id === model)!;

  async function handleGenerate() {
    if (!prompt.trim()) return;
    setLoading(true);
    await new Promise((r) => setTimeout(r, 1500));
    setLoading(false);
  }

  return (
    <div className="p-8 max-w-6xl">
      <div className="mb-8"><h1 className="text-3xl font-black mb-1">Image Generation</h1><p style={{ color: "var(--text-secondary)" }}>Create stunning AI images from text prompts</p></div>
      <div className="flex gap-6">
        <div className="flex-1 flex flex-col gap-5">
          <div className="rounded-2xl p-5" style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}>
            <label className="block text-sm font-semibold mb-3">Prompt</label>
            <textarea className="input-base p-4 text-sm resize-none" rows={4} placeholder="Describe your image…" value={prompt} onChange={(e) => setPrompt(e.target.value)} />
          </div>
          <div className="rounded-2xl p-5" style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}>
            <label className="block text-sm font-semibold mb-4">Style</label>
            <div className="flex flex-wrap gap-2">
              {STYLES.map((s) => (<button key={s} onClick={() => setStyle(s)} className="px-3 py-1.5 rounded-lg text-xs font-medium transition-all" style={{ background: style === s ? "var(--accent)" : "var(--bg-surface)", color: style === s ? "#fff" : "var(--text-secondary)", border: `1px solid ${style === s ? "var(--accent)" : "var(--border)"}`, cursor: "pointer" }}>{s}</button>))}
            </div>
          </div>
          <div className="rounded-2xl p-5" style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}>
            <label className="block text-sm font-semibold mb-4">Size</label>
            <div className="flex flex-wrap gap-2">
              {SIZES.map((s) => (<button key={s} onClick={() => setSize(s)} className="px-3 py-1.5 rounded-lg text-xs font-medium transition-all" style={{ background: size === s ? "var(--accent)" : "var(--bg-surface)", color: size === s ? "#fff" : "var(--text-secondary)", border: `1px solid ${size === s ? "var(--accent)" : "var(--border)"}`, cursor: "pointer" }}>{s}</button>))}
            </div>
          </div>
        </div>
        <div className="w-72 flex flex-col gap-4">
          <div className="rounded-2xl overflow-hidden" style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}>
            <div className="px-5 py-4" style={{ borderBottom: "1px solid var(--border)" }}><span className="text-sm font-semibold">Model</span></div>
            <div className="p-3 flex flex-col gap-2">
              {IMAGE_MODELS.map((m) => (<button key={m.id} onClick={() => setModel(m.id)} className="flex items-start gap-3 px-4 py-3 rounded-xl text-left transition-all w-full" style={{ background: model === m.id ? "var(--accent-dim)" : "var(--bg-surface)", border: `1px solid ${model === m.id ? "var(--accent)" : "transparent"}`, cursor: "pointer" }}>
                <div className="w-3 h-3 rounded-full mt-1 flex-shrink-0 border-2" style={{ borderColor: model === m.id ? "var(--accent-bright)" : "var(--border-bright)", background: model === m.id ? "var(--accent-bright)" : "transparent" }} />
                <div><div className="text-sm font-medium">{m.name}</div><div className="text-xs mt-0.5" style={{ color: "var(--text-muted)" }}>{m.usd} · {m.speed}</div></div>
              </button>))}
            </div>
          </div>
          <div className="rounded-2xl p-5" style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}>
            <div className="flex justify-between text-sm mb-1"><span style={{ color: "var(--text-secondary)" }}>Cost</span><div className="flex items-center gap-1"><Zap size={13} style={{ color: "var(--accent-bright)" }} /><span className="font-bold">{active.credits} credit{active.credits > 1 ? "s" : ""}</span></div></div>
            <div className="text-xs mb-4" style={{ color: "var(--text-muted)" }}>~{active.speed} · {active.usd}</div>
            <button onClick={handleGenerate} disabled={!prompt.trim() || loading} className="btn-primary w-full flex items-center justify-center gap-2 py-3" style={{ opacity: !prompt.trim() || loading ? 0.5 : 1 }}>
              {loading ? "Generating…" : <><ImageIcon size={16} /> Generate Image</>}
            </button>
          </div>
        </div>
      </div>
      <div className="mt-6 rounded-2xl flex items-center justify-center" style={{ background: "var(--bg-card)", border: "1px dashed var(--border)", minHeight: 320 }}>
        <div className="text-center py-16">
          <div className="w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-4" style={{ background: "rgba(245,158,11,0.12)" }}><ImageIcon size={28} style={{ color: "#f59e0b" }} /></div>
          <p className="font-medium mb-1">Your image will appear here</p>
          <p className="text-sm" style={{ color: "var(--text-muted)" }}>Write a prompt and click Generate</p>
        </div>
      </div>
    </div>
  );
}
