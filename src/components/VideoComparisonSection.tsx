import { useRef, useState } from "react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Upload, FileVideo, CheckCircle2, PlayCircle } from "lucide-react";

interface Props {
  fileName: string | null;
  onFile: (name: string) => void;
}

export function VideoComparisonSection({ fileName, onFile }: Props) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [duration] = useState("02:14");

  return (
    <section className="mx-auto mt-10 max-w-7xl px-6">
      <div className="mb-4 flex items-end justify-between">
        <div>
          <h2 className="font-display text-2xl font-bold">Video Analysis</h2>
          <p className="text-sm text-muted-foreground">Original footage vs. AI-annotated tactical output.</p>
        </div>
      </div>

      <div className="grid gap-5 lg:grid-cols-2">
        {/* Original */}
        <div className="glass rounded-2xl p-4">
          <div className="mb-3 flex items-center justify-between">
            <div className="flex items-center gap-2 text-sm font-medium">
              <FileVideo className="h-4 w-4 text-muted-foreground" /> Original Video
            </div>
            <Badge variant="outline" className="border-primary/40 bg-primary/10 text-primary">
              {fileName ? "Ready" : "Awaiting upload"}
            </Badge>
          </div>
          <div className="pitch-bg relative flex aspect-video w-full items-center justify-center overflow-hidden rounded-xl border border-border">
            <input
              ref={inputRef}
              type="file"
              accept="video/*"
              className="hidden"
              onChange={(e) => {
                const f = e.target.files?.[0];
                if (f) onFile(f.name);
              }}
            />
            {fileName ? (
              <PlayCircle className="h-16 w-16 text-white/80 drop-shadow-lg" />
            ) : (
              <Button variant="secondary" onClick={() => inputRef.current?.click()} className="gap-2">
                <Upload className="h-4 w-4" /> Choose file
              </Button>
            )}
          </div>
          <div className="mt-3 flex items-center justify-between text-xs text-muted-foreground">
            <span className="truncate">{fileName ?? "No file selected"}</span>
            <span className="tabular-nums">Duration · {duration}</span>
          </div>
        </div>

        {/* Annotated */}
        <div className="glass rounded-2xl p-4">
          <div className="mb-3 flex items-center justify-between">
            <div className="flex items-center gap-2 text-sm font-medium">
              <CheckCircle2 className="h-4 w-4 text-primary" /> Annotated Tactical Output
            </div>
            <Badge className="bg-accent/20 text-accent hover:bg-accent/30">AI Enhanced</Badge>
          </div>
          <div className="pitch-bg relative aspect-video w-full overflow-hidden rounded-xl border border-border">
            {/* Overlay badges */}
            <div className="absolute left-3 top-3 flex flex-col gap-2">
              <span className="rounded-md bg-black/60 px-2 py-1 text-[11px] font-medium text-white backdrop-blur">
                Possession: <span className="text-[color:var(--team-blue)]">Team Blue</span>
              </span>
              <span className="rounded-md bg-primary/90 px-2 py-1 text-[11px] font-semibold text-primary-foreground">
                Build-Up Detected
              </span>
            </div>
            <span className="absolute right-3 top-3 rounded-md bg-[color:var(--team-red)]/90 px-2 py-1 text-[11px] font-semibold text-white">
              Counterattack Detected
            </span>

            {/* Player markers with tracking lines */}
            <svg className="absolute inset-0 h-full w-full" viewBox="0 0 400 225">
              <path d="M60,170 C120,120 200,100 340,60" stroke="oklch(0.78 0.19 155)" strokeWidth="1.5" strokeDasharray="4 3" fill="none" />
              <path d="M100,60 C160,90 220,150 300,180" stroke="oklch(0.65 0.23 25)" strokeWidth="1.5" strokeDasharray="4 3" fill="none" />
            </svg>
            <span className="absolute left-[15%] top-[75%] flex h-7 w-7 items-center justify-center rounded-full bg-[color:var(--team-blue)] text-[11px] font-bold text-white ring-2 ring-white/40">10</span>
            <span className="absolute left-[50%] top-[50%] flex h-7 w-7 items-center justify-center rounded-full bg-[color:var(--team-blue)] text-[11px] font-bold text-white ring-2 ring-white/40">8</span>
            <span className="absolute left-[85%] top-[25%] flex h-7 w-7 items-center justify-center rounded-full bg-[color:var(--team-blue)] text-[11px] font-bold text-white ring-2 ring-white/40">7</span>
            <span className="absolute left-[25%] top-[25%] flex h-7 w-7 items-center justify-center rounded-full bg-[color:var(--team-red)] text-[11px] font-bold text-white ring-2 ring-white/40">11</span>
            <span className="absolute left-[75%] top-[80%] flex h-7 w-7 items-center justify-center rounded-full bg-[color:var(--team-red)] text-[11px] font-bold text-white ring-2 ring-white/40">9</span>
            <span className="absolute left-[45%] top-[60%] h-2.5 w-2.5 rounded-full bg-white shadow-[0_0_14px_3px_white]" />
          </div>
          <div className="mt-3 grid grid-cols-3 gap-2 text-center text-xs">
            <div className="rounded-lg bg-secondary/60 p-2"><div className="text-muted-foreground">Frames</div><div className="font-semibold tabular-nums">3,214</div></div>
            <div className="rounded-lg bg-secondary/60 p-2"><div className="text-muted-foreground">Tracked</div><div className="font-semibold tabular-nums">22 players</div></div>
            <div className="rounded-lg bg-secondary/60 p-2"><div className="text-muted-foreground">Confidence</div><div className="font-semibold text-primary">94%</div></div>
          </div>
        </div>
      </div>
    </section>
  );
}
