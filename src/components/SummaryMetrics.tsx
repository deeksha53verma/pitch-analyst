import { summaryMetrics } from "@/data/mockData";
import { CircleDot, Route, Zap, User, Target } from "lucide-react";

const iconMap = { "circle-dot": CircleDot, route: Route, zap: Zap, user: User, target: Target };
const toneMap: Record<string, string> = {
  blue: "text-[color:var(--team-blue)] bg-[color:var(--team-blue)]/10 border-[color:var(--team-blue)]/30",
  red: "text-[color:var(--team-red)] bg-[color:var(--team-red)]/10 border-[color:var(--team-red)]/30",
  primary: "text-primary bg-primary/10 border-primary/30",
  accent: "text-accent bg-accent/10 border-accent/30",
};

export function SummaryMetrics() {
  return (
    <section className="mx-auto mt-10 max-w-7xl px-6">
      <div className="grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-6">
        {summaryMetrics.map((m) => {
          const Icon = iconMap[m.icon as keyof typeof iconMap];
          return (
            <div key={m.label} className="glass group rounded-2xl p-4 transition hover:-translate-y-0.5 hover:border-primary/40">
              <div className={`mb-3 inline-flex h-9 w-9 items-center justify-center rounded-lg border ${toneMap[m.tone]}`}>
                <Icon className="h-4 w-4" />
              </div>
              <div className="text-xs uppercase tracking-wider text-muted-foreground">{m.label}</div>
              <div className="mt-1 font-display text-2xl font-bold tabular-nums">{m.value}</div>
            </div>
          );
        })}
      </div>
    </section>
  );
}
