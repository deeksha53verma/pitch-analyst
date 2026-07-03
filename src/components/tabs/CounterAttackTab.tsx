import { counterattacks } from "@/data/mockData";
import { Zap, ArrowRight } from "lucide-react";
import { Badge } from "@/components/ui/badge";

export function CounterAttackTab() {
  return (
    <div className="space-y-5">
      <div className="grid gap-4 md:grid-cols-3">
        <div className="glass rounded-2xl p-5">
          <div className="text-xs uppercase tracking-wider text-muted-foreground">Total Transitions</div>
          <div className="mt-2 font-display text-4xl font-bold">{counterattacks.length}</div>
          <div className="mt-1 text-xs text-muted-foreground">detected across match</div>
        </div>
        <div className="glass rounded-2xl p-5">
          <div className="text-xs uppercase tracking-wider text-muted-foreground">Blue Counters</div>
          <div className="mt-2 font-display text-4xl font-bold text-[color:var(--team-blue)]">
            {counterattacks.filter((c) => c.team.includes("Blue")).length}
          </div>
        </div>
        <div className="glass rounded-2xl p-5">
          <div className="text-xs uppercase tracking-wider text-muted-foreground">Red Counters</div>
          <div className="mt-2 font-display text-4xl font-bold text-[color:var(--team-red)]">
            {counterattacks.filter((c) => c.team.includes("Red")).length}
          </div>
        </div>
      </div>

      <div className="glass rounded-2xl p-5">
        <div className="mb-4 text-sm font-semibold">Transition Timeline</div>
        <div className="relative h-2 w-full rounded-full bg-secondary">
          {counterattacks.map((c, i) => (
            <span key={c.id} className="absolute -top-1 h-4 w-4 -translate-x-1/2 rounded-full ring-4 ring-background"
              style={{ left: `${15 + i * 22}%`, backgroundColor: c.team.includes("Blue") ? "var(--team-blue)" : "var(--team-red)" }}
              title={`${c.id} · ${c.time}`}
            />
          ))}
        </div>
        <div className="mt-2 flex justify-between text-[10px] text-muted-foreground"><span>0'</span><span>45'</span><span>90'</span></div>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        {counterattacks.map((c) => {
          const isBlue = c.team.includes("Blue");
          return (
            <div key={c.id} className="glass rounded-2xl p-5">
              <div className="mb-3 flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className={`flex h-9 w-9 items-center justify-center rounded-lg ${isBlue ? "bg-[color:var(--team-blue)]/15 text-[color:var(--team-blue)]" : "bg-[color:var(--team-red)]/15 text-[color:var(--team-red)]"}`}>
                    <Zap className="h-4 w-4" />
                  </div>
                  <div>
                    <div className="text-xs font-mono uppercase text-muted-foreground">Transition {c.id}</div>
                    <div className="font-display font-semibold" style={{ color: isBlue ? "var(--team-blue)" : "var(--team-red)" }}>{c.team}</div>
                  </div>
                </div>
                <Badge variant="outline" className="font-mono text-xs">{c.time}</Badge>
              </div>
              <div className="flex flex-wrap items-center gap-2 text-xs">
                <span className="rounded-md bg-secondary/70 px-2 py-1">Lane: <span className="font-semibold text-foreground">{c.lane}</span></span>
                <ArrowRight className="h-3 w-3 text-muted-foreground" />
                <span className="rounded-md bg-secondary/70 px-2 py-1">Players: <span className="font-mono">{c.players.join(", ")}</span></span>
              </div>
              <p className="mt-3 text-sm text-muted-foreground">{c.summary}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
