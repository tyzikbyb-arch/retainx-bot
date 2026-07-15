"use client";

import { useState } from "react";
import { Zap, Info, LayoutGrid, Rows, Play } from "lucide-react";

const VIDEO_MODELS = [
  { id: "sora", name: "Sora", provider: "OpenAI", credits: 10, usd: "$0.50", speed: "~8 min", badge: "Best Quality" },
  { id: "kling", name: "Kling 2.0", provider: "Kuaishou", credits: 6, usd: "$0.30", speed: "~4 min", badge: "Popular" },
  { id: "seedance", name: "Seedance 1.0", provider: "ByteDance", credits: 5, usd: "$0.25", speed: "~3 min", badge: "Fast" },
  { id: "wan", name: "WAN 2.1", provider: "Alibaba", credits: 4, usd: "$0.20", speed: "~3 min", badge: "Budget" },
  { id: "ltx", name: "LTX Video", provider: "Lightricks", credits: 3, usd: "$0.15", speed: "~2 min", badge: "Fastest" },
  { id: "minimax", name: "MiniMax Video", provider: "MiniMax", credits: 5, usd: "$0.25", speed: "~5 min", badge: "Cinematic" },
  { id: "heygen", name: "HeyGen Avatar", provider: "HeyGen", credits: 10, usd: "$0.50", speed: "~6 min", badge: "Avatar" },
];

const RATIOS = ["16:9", "9:16", "1:1", "4:3", "3:4"];
const DURATIONS = ["5s", "10s", "15s"];

const badgeColor: Record<string, string> = { "Best Quality": "#7c3aed", "Popular": "#06b6d4", "Fast": "#22c55e", "Fastest": "#22c55e", "Budget": "#f59e0b", "Cinematic": "#ec4899", "Avatar": "#f97316" };

export default function VideoGeneratePage() {
  const [prompt, setPrompt] = useState("");
  const [selectedModel, setSelectedModel] = useState("kling");
  const [ratio, setRatio] = useState("16:9");
  const [duration, setDuration] = useState("5s");
  const [compareMode, setCompareMode] = useState(false);
  const [compareModels, setCompareModels] = useState<string[]>(["kling", "wan"]);
  const [loading, setLoading] = useState(false);

  const active = VIDEO_MODELS.find((m) => m.id === selectedModel)!;

  function toggleCompare(id: string) {
    setCompareModels((prev) => prev.includes(id) ? prev.filter((m) => m !== id) : prev.length < 3 ? [...prev, id] : prev);
  }

  async function handleGenerate() {
    if (!prompt.trim()) return;
    setLoading(true);
    await new Promise((r) => setTimeout(r, 2000));
    setLoading(false);
  }

  return (
    <div className="p-8 max-w-6xl">
      <div className="mb-8 flex items-center justify-between">
        <div><h1 className="text-3xl font-black mb-1">Video Generation</h1><p style={{ color: "var(--text-secondary)" }}>Generate professional AI videos from text</p></div>
        <button onClick={() => setCompareMode(!compareMode)} className="flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium transition-all" style={{ background: compareMode ? "var(--accent-dim)" : "var(--bg-card)", border: `1px solid ${compareMode ? "var(--accent)" : "var(--border)"}`, color: compareMode ? "var(--accent-bright)" : "var(--text-secondary)", cursor: "pointer" }}>
          {compareMode ? <LayoutGrid size={16} /> : <Rows size={16} />}
          {compareMode ? "Compare mode ON" : "Compare models"}
        </button>
      </div>
      <div className="flex gap-6">
        <div className="flex-1 flex flex-col gap-5">
          <div className="rounded-2xl p-5" style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}>
            <label className="block text-sm font-semibold mb-3">Prompt</label>
            <textarea className="input-base p-4 text-sm resize-none" rows={5} placeholder="Describe your video… e.g. 'Cinematic aerial view of a futuristic city at golden hour, dramatic clouds, 8K'" value={prompt} onChange={(e) => setPrompt(e.target.value)} />
            <div className="flex items-center justify-between mt-3">
              <span className="text-xs" style={{ color: "var(--text-muted)" }}>{prompt.length}/500 characters</span>
              <button className="text-xs px-3 py-1.5 rounded-lg" style={{ background: "var(--bg-surface)", color: "var(--accent-bright)", border: "1px solid var(--border)", cursor: "pointer" }}>✨ Enhance prompt</button>
            </div>
          </div>
          <div className="rounded-2xl p-5" style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}>
            <label className="block text-sm font-semibold mb-4">Settings</label>
            <div className="grid grid-cols-2 gap-6">
              <div>
                <span className="text-xs font-medium mb-2 block" style={{ color: "var(--text-secondary)" }}>Aspect Ratio</span>
                <div className="flex flex-wrap gap-2">
                  {RATIOS.map((r) => (<button key={r} onClick={() => setRatio(r)} className="px-3 py-1.5 rounded-lg text-xs font-medium transition-all" style={{ background: ratio === r ? "var(--accent)" : "var(--bg-surface)", color: ratio === r ? "#fff" : "var(--text-secondary)", border: `1px solid ${ratio === r ? "var(--accent)" : "var(--border)"}`, cursor: "pointer" }}>{r}</button>))}
                </div>
              </div>
              <div>
                <span className="text-xs font-medium mb-2 block" style={{ color: "var(--text-secondary)" }}>Duration</span>
                <div className="flex gap-2">
                  {DURATIONS.map((d) => (<button key={d} onClick={() => setDuration(d)} className="px-3 py-1.5 rounded-lg text-xs font-medium transition-all" style={{ background: duration === d ? "var(--accent)" : "var(--bg-surface)", color: duration === d ? "#fff" : "var(--text-secondary)", border: `1px solid ${duration === d ? "var(--accent)" : "var(--border)"}`, cursor: "pointer" }}>{d}</button>))}
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="w-72 flex flex-col gap-4">
          <div className="rounded-2xl overflow-hidden" style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}>
            <div className="px-5 py-4" style={{ borderBottom: "1px solid var(--border)" }}><span className="text-sm font-semibold">{compareMode ? "Select up to 3 models" : "Select model"}</span></div>
            <div className="p-3 flex flex-col gap-2 max-h-80 overflow-y-auto">
              {VIDEO_MODELS.map((m) => {
                const isActive = compareMode ? compareModels.includes(m.id) : selectedModel === m.id;
                return (
                  <button key={m.id} onClick={() => compareMode ? toggleCompare(m.id) : setSelectedModel(m.id)} className="flex items-start gap-3 px-4 py-3 rounded-xl text-left transition-all w-full" style={{ background: isActive ? "var(--accent-dim)" : "var(--bg-surface)", border: `1px solid ${isActive ? "var(--accent)" : "transparent"}`, cursor: "pointer" }}>
                    <div className="w-3 h-3 rounded-full mt-1 flex-shrink-0 border-2 transition-all" style={{ borderColor: isActive ? "var(--accent-bright)" : "var(--border-bright)", background: isActive ? "var(--accent-bright)" : "transparent" }} />
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 flex-wrap">
                        <span className="text-sm font-medium">{m.name}</span>
                        <span className="text-[10px] font-bold px-1.5 py-0.5 rounded" style={{ background: (badgeColor[m.badge] || "#7c3aed") + "22", color: badgeColor[m.badge] || "#7c3aed" }}>{m.badge}</span>
                      </div>
                      <div className="text-xs mt-0.5" style={{ color: "var(--text-muted)" }}>{m.usd} · {m.speed}</div>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
          <div className="rounded-2xl p-5" style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}>
            {compareMode ? (
              <div className="mb-4">
                <div className="text-xs font-medium mb-2" style={{ color: "var(--text-secondary)" }}>Cost per model</div>
                {compareModels.map((id) => { const m = VIDEO_MODELS.find((x) => x.id === id)!; return (<div key={id} className="flex justify-between text-sm py-1"><span style={{ color: "var(--text-secondary)" }}>{m.name}</span><span className="font-semibold">{m.credits} cr</span></div>); })}
                <div className="flex justify-between text-sm font-bold pt-2 mt-2" style={{ borderTop: "1px solid var(--border)" }}>
                  <span>Total</span><span style={{ color: "var(--accent-bright)" }}>{compareModels.reduce((sum, id) => sum + (VIDEO_MODELS.find((m) => m.id === id)?.credits || 0), 0)} cr</span>
                </div>
              </div>
            ) : (
              <div className="mb-4">
                <div className="flex items-center justify-between text-sm mb-1"><span style={{ color: "var(--text-secondary)" }}>Cost</span><div className="flex items-center gap-1"><Zap size={13} style={{ color: "var(--accent-bright)" }} /><span className="font-bold">{active.credits} credits</span></div></div>
                <div className="flex items-center justify-between text-xs"><span style={{ color: "var(--text-muted)" }}>~{active.speed}</span><span style={{ color: "var(--text-muted)" }}>{active.usd}</span></div>
                <div className="flex items-center gap-1 mt-2 text-xs" style={{ color: "var(--text-muted)" }}><Info size={11} />You have 42 credits remaining</div>
              </div>
            )}
            <button onClick={handleGenerate} disabled={!prompt.trim() || loading} className="btn-primary w-full flex items-center justify-center gap-2 py-3" style={{ opacity: !prompt.trim() || loading ? 0.5 : 1 }}>
              {loading ? <><div className="w-4 h-4 rounded-full border-2 border-white/20 border-t-white animate-spin" />Generating…</> : <><Play size={16} />{compareMode ? `Compare ${compareModels.length} Models` : "Generate Video"}</>}
            </button>
          </div>
        </div>
      </div>
      <div className="mt-6 rounded-2xl flex items-center justify-center" style={{ background: "var(--bg-card)", border: "1px dashed var(--border)", minHeight: 280 }}>
        <div className="text-center py-16">
          <div className="w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-4" style={{ background: "var(--accent-dim)" }}><Play size={28} style={{ color: "var(--accent-bright)" }} /></div>
          <p className="font-medium mb-1">Your video will appear here</p>
          <p className="text-sm" style={{ color: "var(--text-muted)" }}>Write a prompt and click Generate</p>
        </div>
      </div>
    </div>
  );
}
