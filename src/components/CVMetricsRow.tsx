import { useAnalysis } from "@/hooks/useAnalysis";
import { Scan, Users, Aperture, RefreshCw, Route, Zap } from "lucide-react";

export function CVMetricsRow() {
  const { data } = useAnalysis();
  const metrics = [
    { label: "Players Tracked", value: `${data.players.length}`, sub: "99% confidence", icon: Users },
    { label: "Jersey IDs", value: `${data.players.filter(p => p.num).length}`, sub: "Recognized", icon: Scan },
    { label: "Ball Tracking", value: "94%", sub: "Frames active", icon: Aperture },
    { label: "Possession Changes", value: `${data.possessionEvents.length}`, sub: "Total", icon: RefreshCw },
    { label: "Build-Ups", value: `${data.buildUps.length}`, sub: "Sequences", icon: Route },
    { label: "Transitions", value: `${data.counterattacks.length}`, sub: "Counterattacks", icon: Zap },
  ];

  return (
    <section className="mx-auto mt-6 max-w-7xl px-6">
      <div className="mb-3">
        <h3 className="font-display text-sm font-semibold uppercase tracking-wider text-muted-foreground">Computer Vision Pipeline Outputs</h3>
      </div>
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-6">
        {metrics.map((m, i) => (
          <div key={i} className="glass rounded-xl p-4 flex flex-col items-center text-center">
            <m.icon className="h-5 w-5 text-primary mb-2" />
            <div className="text-xl font-bold tabular-nums">{m.value}</div>
            <div className="text-[11px] font-medium leading-tight mt-1">{m.label}</div>
            <div className="text-[10px] text-muted-foreground mt-1">{m.sub}</div>
          </div>
        ))}
      </div>
    </section>
  );
}
