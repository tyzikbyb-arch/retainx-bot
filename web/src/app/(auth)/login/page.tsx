"use client";

import Link from "next/link";
import { useState } from "react";
import { Eye, EyeOff, ArrowRight } from "lucide-react";

export default function LoginPage() {
  const [show, setShow] = useState(false);
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({ email: "", password: "" });

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    await new Promise((r) => setTimeout(r, 1000));
    setLoading(false);
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-4" style={{ background: "var(--bg)" }}>
      <div className="fixed pointer-events-none" style={{ width: 500, height: 500, borderRadius: "50%", background: "var(--accent)", opacity: 0.06, filter: "blur(100px)", top: "30%", left: "50%", transform: "translateX(-50%)" }} />
      <div className="relative z-10 w-full max-w-md">
        <div className="text-center mb-8">
          <Link href="/" className="inline-flex items-center gap-2 font-bold text-xl" style={{ textDecoration: "none" }}>
            <div className="w-9 h-9 rounded-xl flex items-center justify-center text-white font-black" style={{ background: "linear-gradient(135deg,#7c3aed,#06b6d4)" }}>R</div>
            <span className="gradient-text">RetainX Studio</span>
          </Link>
          <h1 className="mt-6 text-2xl font-bold">Welcome back</h1>
          <p className="mt-2 text-sm" style={{ color: "var(--text-secondary)" }}>Sign in to continue generating</p>
        </div>
        <div className="rounded-2xl p-8" style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}>
          <form onSubmit={handleSubmit} className="flex flex-col gap-5">
            <div className="flex flex-col gap-2">
              <label className="text-sm font-medium" style={{ color: "var(--text-secondary)" }}>Email</label>
              <input type="email" required placeholder="you@example.com" className="input-base px-4 py-3 text-sm" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-sm font-medium" style={{ color: "var(--text-secondary)" }}>Password</label>
              <div className="relative">
                <input type={show ? "text" : "password"} required placeholder="••••••••" className="input-base px-4 py-3 text-sm pr-11" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} />
                <button type="button" onClick={() => setShow(!show)} className="absolute right-3 top-1/2 -translate-y-1/2" style={{ color: "var(--text-muted)", background: "none", border: "none", cursor: "pointer" }}>
                  {show ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
            </div>
            <button type="submit" disabled={loading} className="btn-primary flex items-center justify-center gap-2 py-3 text-sm mt-2" style={{ opacity: loading ? 0.7 : 1 }}>
              {loading ? "Signing in…" : <><>Sign In</> <ArrowRight size={16} /></>}
            </button>
          </form>
          <div className="mt-6 pt-6" style={{ borderTop: "1px solid var(--border)" }}>
            <p className="text-sm text-center" style={{ color: "var(--text-muted)" }}>
              Don&apos;t have an account?{" "}
              <Link href="/register" style={{ color: "var(--accent-bright)", textDecoration: "none", fontWeight: 600 }}>Sign up free</Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
