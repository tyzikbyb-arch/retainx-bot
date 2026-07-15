"use client";

import Link from "next/link";
import { useState } from "react";
import { Eye, EyeOff, ArrowRight, Check } from "lucide-react";

const PERKS = [
  "20 free credits on signup",
  "15+ AI models available",
  "No subscription required",
  "Commercial rights on all generations",
];

export default function RegisterPage() {
  const [show, setShow] = useState(false);
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({ name: "", email: "", password: "" });

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    await new Promise((r) => setTimeout(r, 1200));
    setLoading(false);
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-12" style={{ background: "var(--bg)" }}>
      <div className="relative z-10 w-full max-w-4xl flex flex-col md:flex-row gap-8 items-start">
        <div className="flex-1 md:pt-8">
          <Link href="/" className="inline-flex items-center gap-2 font-bold text-xl mb-8 block" style={{ textDecoration: "none" }}>
            <div className="w-9 h-9 rounded-xl flex items-center justify-center text-white font-black" style={{ background: "linear-gradient(135deg,#7c3aed,#06b6d4)" }}>R</div>
            <span className="gradient-text">RetainX Studio</span>
          </Link>
          <h1 className="text-3xl font-black mb-4">Start creating with<br /><span className="gradient-text">every AI model</span></h1>
          <p className="mb-8" style={{ color: "var(--text-secondary)" }}>One account. 15+ models. Pay only when you create.</p>
          <div className="flex flex-col gap-4">
            {PERKS.map((p) => (
              <div key={p} className="flex items-center gap-3">
                <div className="w-5 h-5 rounded-full flex items-center justify-center flex-shrink-0" style={{ background: "rgba(34,197,94,0.15)", color: "#22c55e" }}><Check size={12} /></div>
                <span className="text-sm" style={{ color: "var(--text-secondary)" }}>{p}</span>
              </div>
            ))}
          </div>
        </div>
        <div className="w-full md:w-96 rounded-2xl p-8" style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}>
          <h2 className="text-xl font-bold mb-6">Create your account</h2>
          <form onSubmit={handleSubmit} className="flex flex-col gap-5">
            <div className="flex flex-col gap-2">
              <label className="text-sm font-medium" style={{ color: "var(--text-secondary)" }}>Display name</label>
              <input type="text" required placeholder="Your name" className="input-base px-4 py-3 text-sm" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-sm font-medium" style={{ color: "var(--text-secondary)" }}>Email</label>
              <input type="email" required placeholder="you@example.com" className="input-base px-4 py-3 text-sm" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-sm font-medium" style={{ color: "var(--text-secondary)" }}>Password</label>
              <div className="relative">
                <input type={show ? "text" : "password"} required minLength={8} placeholder="At least 8 characters" className="input-base px-4 py-3 text-sm pr-11" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} />
                <button type="button" onClick={() => setShow(!show)} className="absolute right-3 top-1/2 -translate-y-1/2" style={{ color: "var(--text-muted)", background: "none", border: "none", cursor: "pointer" }}>{show ? <EyeOff size={16} /> : <Eye size={16} />}</button>
              </div>
            </div>
            <button type="submit" disabled={loading} className="btn-primary flex items-center justify-center gap-2 py-3 text-sm mt-2" style={{ opacity: loading ? 0.7 : 1 }}>
              {loading ? "Creating account…" : <><>Create Free Account</> <ArrowRight size={16} /></>}
            </button>
            <p className="text-xs text-center" style={{ color: "var(--text-muted)" }}>By signing up you agree to our terms of service.</p>
          </form>
          <div className="mt-6 pt-6" style={{ borderTop: "1px solid var(--border)" }}>
            <p className="text-sm text-center" style={{ color: "var(--text-muted)" }}>Already have an account?{" "}<Link href="/login" style={{ color: "var(--accent-bright)", textDecoration: "none", fontWeight: 600 }}>Sign in</Link></p>
          </div>
        </div>
      </div>
    </div>
  );
}
