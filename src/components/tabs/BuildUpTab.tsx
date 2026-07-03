import { buildUps } from "@/data/mockData";
import { ArrowRight, Users } from "lucide-react";
import { Badge } from "@/components/ui/badge";

export function BuildUpTab() {
  return (
    <div className="grid gap-4 md:grid-cols-2">
      {buildUps.map((b) => {
        const isBlue = b.team.includes("Blue");
        return (
          <div key={b.id} className="glass rounded-2xl p-5">
            <div className="mb-3 flex items-start justify-between">
              <div>
                <div className="text-xs font-mono uppercase text-muted-foreground">{b.id}</div>
                <div className="font-display text-lg font-semibold">
                  <span className={isBlue ? "text-[color:var(--team-blue)]" : "text-[color:var(--team-red)]"}>{b.team}</span>{" "}
                  build-up
                </div>
              </div>
              <Badge variant="outline" className="font-mono text-xs">{b.start} → {b.end}</Badge>
            </div>

            <div className="mb-3 flex flex-wrap items-center gap-1.5 text-xs">
              {b.path.map((p, i) => (
                <span key={i} className="flex items-center gap-1.5">
                  <span className="rounded-md bg-secondary/70 px-2 py-1 font-medium">{p}</span>
                  {i < b.path.length - 1 && <ArrowRight className="h-3 w-3 text-muted-foreground" />}
                </span>
              ))}
            </div>

            <div className="pitch-bg relative h-24 overflow-hidden rounded-lg border border-border">
              <svg className="absolute inset-0 h-full w-full" viewBox="0 0 400 100" preserveAspectRatio="none">
                <path d="M20,80 C120,80 180,20 380,25" stroke={isBlue ? "oklch(0.68 0.19 245)" : "oklch(0.65 0.23 25)"} strokeWidth="2" strokeDasharray="5 4" fill="none" />
                <circle cx="20" cy="80" r="4" fill="oklch(0.78 0.19 155)" />
                <circle cx="200" cy="52" r="4" fill="oklch(0.78 0.19 155)" />
                <circle cx="380" cy="25" r="5" fill="white" />
              </svg>
            </div>

            <div className="mt-3 flex items-center justify-between text-xs">
              <div className="flex items-center gap-2 text-muted-foreground">
                <Users className="h-3.5 w-3.5" /> {b.players.join(" · ")}
              </div>
              <span className="rounded-md bg-primary/15 px-2 py-1 font-medium text-primary">{b.outcome}</span>
            </div>
          </div>
        );
      })}
    </div>
  );
}
