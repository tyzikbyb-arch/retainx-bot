"use client";

import { useState } from "react";
import { Zap, CreditCard, Check } from "lucide-react";

const PACKS = [
  { credits: 20, usd: 1.0, label: "$1", tag: "" },
  { credits: 100, usd: 5.0, label: "$5", tag: "Popular" },
  { credits: 200, usd: 10.0, label: "$10", tag: "" },
  { credits: 500, usd: 25.0, label: "$25", tag: "Best Value" },
  { credits: 1000, usd: 45.0, label: "$45", tag: "10% off" },
  { credits: 2000, usd: 80.0, label: "$80", tag: "20% off" },
];

const HISTORY = [
  { type: "purchase", desc: "Credit top-up (+100 cr)", amount: "+100", usd: "$5.00", date: "Jul 12, 2025" },
  { type: "spend", desc: "Video — Kling 2.0", amount: "-6", usd: "-$0.30", date: "Jul 12, 2025" },
  { type: "spend", desc: "Image — Grok Aurora", amount: "-1", usd: "-$0.05", date: "Jul 11, 2025" },
  { type: "spend", desc: "Video — WAN 2.1", amount: "-4", usd: "-$0.20", date: "Jul 10, 2025" },
  { type: "purchase", desc: "Credit top-up (+20 cr)", amount: "+20", usd: "$1.00", date: "Jul 9, 2025" },
];

export default function BillingPage() {
  const [selected, setSelected] = useState(1);
  const [loading, setLoading] = useState(false);

  async function handleCheckout() {
    setLoading(true);
    await new Promise((r) => setTimeout(r, 1200));
    setLoading(false);
  }

  return (
    <div className="p-8 max-w-3xl">
      <div className="mb-8"><h1 className="text-3xl font-black mb-1">Billing & Credits</h1><p style={{ color: "var(--text-secondary)" }}>Buy credits. Pay only for what you generate.</p></div>
      <div className="rounded-2xl p-6 mb-8 flex items-center justify-between" style={{ background: "var(--accent-dim)", border: "1px solid var(--accent)" }}>
        <div>
          <div className="text-sm font-medium mb-1" style={{ color: "var(--accent-bright)" }}>Current Balance</div>
          <div className="text-4xl font-black flex items-center gap-2"><Zap size={28} style={{ color: "var(--accent-bright)" }} />42 credits</div>
          <div className="text-sm mt-1" style={{ color: "var(--text-muted)" }}>≈ $2.10 · 1 credit = $0.05</div>
        </div>
        <div className="text-right">
          <div className="text-xs mb-2" style={{ color: "var(--text-muted)" }}>What can you make?</div>
          <div className="text-sm" style={{ color: "var(--text-secondary)" }}>~7 videos (Kling)</div>
          <div className="text-sm" style={{ color: "var(--text-secondary)" }}>~42 images</div>
          <div className="text-sm" style={{ color: "var(--text-secondary)" }}>~21 audio files</div>
        </div>
      </div>
      <h2 className="text-xl font-bold mb-5">Top up credits</h2>
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-8">
        {PACKS.map((p, i) => (
          <button key={i} onClick={() => setSelected(i)} className="relative rounded-2xl p-5 text-left transition-all" style={{ background: selected === i ? "var(--accent-dim)" : "var(--bg-card)", border: `2px solid ${selected === i ? "var(--accent)" : "var(--border)"}`, cursor: "pointer" }}>
            {p.tag && <div className="absolute -top-3 left-4 text-xs font-bold px-3 py-0.5 rounded-full" style={{ background: "var(--accent)", color: "#fff" }}>{p.tag}</div>}
            {selected === i && <div className="absolute top-3 right-3 w-5 h-5 rounded-full flex items-center justify-center" style={{ background: "var(--accent)" }}><Check size={11} color="#fff" /></div>}
            <div className="text-2xl font-black mb-1" style={{ color: selected === i ? "var(--accent-bright)" : "var(--text-primary)" }}>{p.credits}</div>
            <div className="text-xs mb-2" style={{ color: "var(--text-muted)" }}>credits</div>
            <div className="text-lg font-bold">{p.label}</div>
          </button>
        ))}
      </div>
      <button onClick={handleCheckout} disabled={loading} className="btn-primary w-full flex items-center justify-center gap-3 py-4 text-base mb-10" style={{ opacity: loading ? 0.7 : 1 }}>
        <CreditCard size={20} />{loading ? "Redirecting to Stripe…" : `Buy ${PACKS[selected].credits} credits for ${PACKS[selected].label}`}
      </button>
      <h2 className="text-xl font-bold mb-5">Transaction History</h2>
      <div className="rounded-2xl overflow-hidden" style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}>
        {HISTORY.map((h, i) => (
          <div key={i} className="flex items-center justify-between px-6 py-4" style={{ borderBottom: i < HISTORY.length - 1 ? "1px solid var(--border)" : "none" }}>
            <div className="flex items-center gap-4">
              <div className="w-9 h-9 rounded-xl flex items-center justify-center" style={{ background: h.type === "purchase" ? "rgba(34,197,94,0.12)" : "var(--accent-dim)", color: h.type === "purchase" ? "#22c55e" : "var(--accent-bright)" }}>
                {h.type === "purchase" ? <Zap size={16} /> : <CreditCard size={16} />}
              </div>
              <div><div className="text-sm font-medium">{h.desc}</div><div className="text-xs" style={{ color: "var(--text-muted)" }}>{h.date}</div></div>
            </div>
            <div className="text-right">
              <div className="text-sm font-bold" style={{ color: h.type === "purchase" ? "#22c55e" : "var(--text-primary)" }}>{h.amount} cr</div>
              <div className="text-xs" style={{ color: "var(--text-muted)" }}>{h.usd}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
