"use client";

import { useState } from "react";
import { Mic, Zap, Play } from "lucide-react";

const VOICE_MODELS = [
  { id: "eleven", name: "ElevenLabs", credits: 2, usd: "$0.10", speed: "~30s", badge: "Best Voice" },
  { id: "cartesia", name: "Cartesia", credits: 2, usd: "$0.10", speed: "~20s", badge: "Fast" },
];

const VOICES = ["Professional Male", "Professional Female", "Narrator", "News Anchor", "Casual Male", "Casual Female"];
const LANGUAGES = ["English", "Russian", "Arabic", "Spanish", "French", "German"];

export default function AudioGeneratePage() {
  const [text, setText] = useState("");
  const [model, setModel] = useState("eleven");
  const [voice, setVoice] = useState("Professional Male");
  const [lang, setLang] = useState("English");
  const [loading, setLoading] = useState(false);

  const active = VOICE_MODELS.find((m) => m.id === model)!;

  async function handleGenerate() {
    if (!text.trim()) return;
    setLoading(true);
    await new Promise((r) => setTimeout(r, 1200));
    setLoading(false);
  }

  return (
    <div className="p-8 max-w-5xl">
      <div className="mb-8"><h1 className="text-3xl font-black mb-1">Audio Generation</h1><p style={{ color: "var(--text-secondary)" }}>Convert text to natural-sounding voice with AI</p></div>
      <div className="flex gap-6">
        <div className="flex-1 flex flex-col gap-5">
          <div className="rounded-2xl p-5" style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}>
            <label className="block text-sm font-semibold mb-3">Text to convert</label>
            <textarea className="input-base p-4 text-sm resize-none" rows={6} placeholder="Enter the text you want to convert to speech…" value={text} onChange={(e) => setText(e.target.value)} />
            <div className="text-xs mt-2" style={{ color: "var(--text-muted)" }}>{text.length} / 5000 characters</div>
          </div>
          <div className="rounded-2xl p-5" style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}>
            <label className="block text-sm font-semibold mb-4">Voice</label>
            <div className="flex flex-wrap gap-2 mb-5">
              {VOICES.map((v) => (<button key={v} onClick={() => setVoice(v)} className="px-3 py-1.5 rounded-lg text-xs font-medium transition-all" style={{ background: voice === v ? "#06b6d422" : "var(--bg-surface)", color: voice === v ? "#06b6d4" : "var(--text-secondary)", border: `1px solid ${voice === v ? "#06b6d444" : "var(--border)"}`, cursor: "pointer" }}>{v}</button>))}
            </div>
            <label className="block text-sm font-semibold mb-3">Language</label>
            <div className="flex flex-wrap gap-2">
              {LANGUAGES.map((l) => (<button key={l} onClick={() => setLang(l)} className="px-3 py-1.5 rounded-lg text-xs font-medium transition-all" style={{ background: lang === l ? "#06b6d422" : "var(--bg-surface)", color: lang === l ? "#06b6d4" : "var(--text-secondary)", border: `1px solid ${lang === l ? "#06b6d444" : "var(--border)"}`, cursor: "pointer" }}>{l}</button>))}
            </div>
          </div>
        </div>
        <div className="w-72 flex flex-col gap-4">
          <div className="rounded-2xl overflow-hidden" style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}>
            <div className="px-5 py-4" style={{ borderBottom: "1px solid var(--border)" }}><span className="text-sm font-semibold">Voice Model</span></div>
            <div className="p-3 flex flex-col gap-2">
              {VOICE_MODELS.map((m) => (<button key={m.id} onClick={() => setModel(m.id)} className="flex items-start gap-3 px-4 py-3 rounded-xl text-left w-full transition-all" style={{ background: model === m.id ? "rgba(6,182,212,0.1)" : "var(--bg-surface)", border: `1px solid ${model === m.id ? "#06b6d444" : "transparent"}`, cursor: "pointer" }}>
                <div className="w-3 h-3 rounded-full mt-1 border-2 flex-shrink-0" style={{ borderColor: model === m.id ? "#06b6d4" : "var(--border-bright)", background: model === m.id ? "#06b6d4" : "transparent" }} />
                <div><div className="text-sm font-medium">{m.name}</div><div className="text-xs mt-0.5" style={{ color: "var(--text-muted)" }}>{m.usd} · {m.speed}</div></div>
              </button>))}
            </div>
          </div>
          <div className="rounded-2xl p-5" style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}>
            <div className="flex justify-between text-sm mb-4"><span style={{ color: "var(--text-secondary)" }}>Cost</span><div className="flex items-center gap-1"><Zap size={13} style={{ color: "#06b6d4" }} /><span className="font-bold">{active.credits} credits</span></div></div>
            <button onClick={handleGenerate} disabled={!text.trim() || loading} className="w-full flex items-center justify-center gap-2 py-3 rounded-xl font-semibold text-sm transition-all" style={{ background: "#06b6d4", color: "#fff", border: "none", cursor: !text.trim() || loading ? "default" : "pointer", opacity: !text.trim() || loading ? 0.5 : 1 }}>
              {loading ? "Generating…" : <><Mic size={16} /> Generate Audio</>}
            </button>
          </div>
        </div>
      </div>
      <div className="mt-6 rounded-2xl flex items-center justify-center" style={{ background: "var(--bg-card)", border: "1px dashed var(--border)", minHeight: 180 }}>
        <div className="text-center py-12">
          <div className="w-14 h-14 rounded-2xl flex items-center justify-center mx-auto mb-4" style={{ background: "rgba(6,182,212,0.12)" }}><Play size={24} style={{ color: "#06b6d4" }} /></div>
          <p className="font-medium mb-1">Audio player will appear here</p>
          <p className="text-sm" style={{ color: "var(--text-muted)" }}>Enter text and click Generate</p>
        </div>
      </div>
    </div>
  );
}
