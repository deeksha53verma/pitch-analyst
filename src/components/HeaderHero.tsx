import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Activity, Upload, Play, Sparkles } from "lucide-react";

interface Props {
  onUpload: () => void;
  onDemo: () => void;
  onRun: () => void;
  analyzed: boolean;
  analyzing?: boolean;
}

export function HeaderHero({ onUpload, onDemo, onRun, analyzed, analyzing }: Props) {
  return (
    <header className="relative overflow-hidden border-b border-border">
      <div className="absolute inset-0 pitch-bg opacity-[0.08]" aria-hidden />
      <div className="absolute -top-32 -right-24 h-96 w-96 rounded-full bg-primary/20 blur-3xl" aria-hidden />
      <div className="absolute -bottom-24 -left-24 h-80 w-80 rounded-full bg-accent/20 blur-3xl" aria-hidden />

      <div className="relative mx-auto max-w-7xl px-6 py-10">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-primary to-accent shadow-lg shadow-primary/20">
              <Activity className="h-5 w-5 text-primary-foreground" />
            </div>
            <div>
              <div className="font-display text-lg font-bold tracking-tight">MatchMind</div>
              <div className="text-xs text-muted-foreground">Tactical Intelligence</div>
            </div>
          </div>
          <Badge variant="outline" className="hidden gap-1.5 border-primary/40 bg-primary/10 text-primary md:inline-flex">
            <Sparkles className="h-3 w-3" /> AI-Powered Match Analysis
          </Badge>
        </div>

        <div className="mt-10 grid gap-8 lg:grid-cols-[1.4fr_1fr] lg:items-center">
          <div>
            <h1 className="font-display text-4xl font-bold leading-[1.05] tracking-tight md:text-5xl lg:text-6xl">
              Football <span className="text-gradient-accent">Tactical Intelligence</span> Dashboard
            </h1>
            <p className="mt-5 max-w-2xl text-base leading-relaxed text-muted-foreground md:text-lg">
              Upload a football match clip and analyze player identity, possession, build-up sequences,
              team compactness, positional tendencies, and transition events — all in one AI-powered workstation.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              {!analyzed && (
                <>
                  <Button size="lg" onClick={onUpload} disabled={analyzing} className="gap-2">
                    <Upload className="h-4 w-4" /> Upload Video
                  </Button>
                  <Button size="lg" variant="secondary" onClick={onDemo} disabled={analyzing} className="gap-2">
                    <Play className="h-4 w-4" /> Use Demo Match
                  </Button>
                  <Button size="lg" variant="outline" onClick={onRun} disabled={analyzing} className="gap-2 border-primary/50 text-primary hover:bg-primary/10 hover:text-primary">
                    <Sparkles className="h-4 w-4" /> Run Analysis
                  </Button>
                </>
              )}
              {analyzed && (
                <>
                  <Button size="sm" variant="secondary" className="gap-2 text-xs">
                    Download Annotated Video
                  </Button>
                  <Button size="sm" variant="secondary" className="gap-2 text-xs">
                    Download Possession CSV
                  </Button>
                  <Button size="sm" variant="secondary" className="gap-2 text-xs">
                    Download Tactical Report
                  </Button>
                </>
              )}
            </div>
          </div>

          <div className="glass relative rounded-2xl p-5">
            <div className="mb-3 flex items-center justify-between">
              <div className="text-xs uppercase tracking-widest text-muted-foreground">Live Match Signal</div>
              <div className="flex items-center gap-1.5 text-xs text-primary">
                <span className="h-2 w-2 animate-pulse rounded-full bg-primary" /> streaming
              </div>
            </div>
            <div className="pitch-bg relative aspect-[16/10] w-full overflow-hidden rounded-xl border border-border">
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="h-24 w-24 rounded-full border-2 border-white/40" />
              </div>
              <span className="absolute left-4 top-4 flex h-6 w-6 items-center justify-center rounded-full bg-[color:var(--team-blue)] text-[10px] font-bold text-white">10</span>
              <span className="absolute right-8 top-10 flex h-6 w-6 items-center justify-center rounded-full bg-[color:var(--team-red)] text-[10px] font-bold text-white">9</span>
              <span className="absolute bottom-6 left-1/3 flex h-6 w-6 items-center justify-center rounded-full bg-[color:var(--team-blue)] text-[10px] font-bold text-white">8</span>
              <span className="absolute bottom-10 right-1/3 flex h-6 w-6 items-center justify-center rounded-full bg-[color:var(--team-red)] text-[10px] font-bold text-white">11</span>
              <span className="absolute left-1/2 top-1/2 h-2 w-2 -translate-x-1/2 -translate-y-1/2 rounded-full bg-white shadow-[0_0_12px_2px_white]" />
            </div>
            <div className="mt-3 grid grid-cols-3 gap-2 text-center">
              <div className="rounded-lg bg-secondary/60 p-2">
                <div className="text-[10px] uppercase text-muted-foreground">Possession</div>
                <div className="text-sm font-semibold text-[color:var(--team-blue)]">Blue</div>
              </div>
              <div className="rounded-lg bg-secondary/60 p-2">
                <div className="text-[10px] uppercase text-muted-foreground">Phase</div>
                <div className="text-sm font-semibold">Build-Up</div>
              </div>
              <div className="rounded-lg bg-secondary/60 p-2">
                <div className="text-[10px] uppercase text-muted-foreground">xT</div>
                <div className="text-sm font-semibold text-primary">+0.14</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
