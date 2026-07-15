import { Video, Image as ImageIcon, Mic, Download, RefreshCw } from "lucide-react";

const HISTORY = [
  { id: 1, type: "video", model: "Kling 2.0", prompt: "Cyberpunk city at night, rain reflections", credits: 6, date: "Jul 12, 2025 · 14:32", meta: "5s · 16:9" },
  { id: 2, type: "image", model: "Grok Aurora", prompt: "Abstract golden waves on deep space background", credits: 1, date: "Jul 12, 2025 · 09:15", meta: "1024×1024" },
  { id: 3, type: "video", model: "WAN 2.1", prompt: "Ocean waves crashing on rocky shore, slow motion", credits: 4, date: "Jul 11, 2025 · 21:04", meta: "10s · 16:9" },
  { id: 4, type: "audio", model: "ElevenLabs", prompt: "Professional voice for travel documentary", credits: 2, date: "Jul 10, 2025 · 16:48", meta: "" },
  { id: 5, type: "video", model: "Sora", prompt: "Aerial shot of mountain peaks at sunrise", credits: 10, date: "Jul 9, 2025 · 11:22", meta: "5s · 16:9" },
];

const typeColor: Record<string, string> = { video: "#7c3aed", image: "#f59e0b", audio: "#06b6d4" };

export default function HistoryPage() {
  return (
    <div className="p-8 max-w-4xl">
      <div className="mb-8">
        <h1 className="text-3xl font-black mb-1">Generation History</h1>
        <p style={{ color: "var(--text-secondary)" }}>All your past creations in one place</p>
      </div>
      <div className="flex flex-col gap-3">
        {HISTORY.map((item) => (
          <div key={item.id} className="rounded-2xl p-5 flex items-center gap-5" style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}>
            <div className="w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0" style={{ background: typeColor[item.type]+"22", color: typeColor[item.type] }}>
              {item.type==="video"?<Video size={20}/>:item.type==="image"?<ImageIcon size={20}/>:<Mic size={20}/>}
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-sm font-semibold">{item.model}</span>
                {item.meta && <span className="text-[10px]" style={{ color: "var(--text-muted)" }}>{item.meta}</span>}
              </div>
              <p className="text-sm truncate" style={{ color: "var(--text-secondary)" }}>{item.prompt}</p>
              <p className="text-xs mt-1" style={{ color: "var(--text-muted)" }}>{item.date}</p>
            </div>
            <div className="text-sm font-bold flex-shrink-0" style={{ color: "var(--text-muted)" }}>{item.credits} cr</div>
            <div className="text-xs font-medium px-2.5 py-1 rounded-full flex-shrink-0" style={{ background: "rgba(34,197,94,0.12)", color: "#22c55e" }}>Done</div>
            <div className="flex gap-2 flex-shrink-0">
              <button className="w-9 h-9 rounded-xl flex items-center justify-center" style={{ background: "var(--bg-surface)", border: "1px solid var(--border)", cursor: "pointer", color: "var(--text-muted)" }}><Download size={15} /></button>
              <button className="w-9 h-9 rounded-xl flex items-center justify-center" style={{ background: "var(--bg-surface)", border: "1px solid var(--border)", cursor: "pointer", color: "var(--text-muted)" }}><RefreshCw size={15} /></button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
