import { Brain, ShieldAlert, Target, TrendingUp } from "lucide-react";
import { useAnalysis } from "@/hooks/useAnalysis";

export function PredictiveTab() {
  const { data } = useAnalysis();
  const predictive = data?.predictive ?? [];

  if (predictive.length === 0) {
    return (
      <div className="glass rounded-2xl p-8 text-center">
        <div className="text-muted-foreground">No predictive intelligence data.</div>
        <div className="text-xs text-muted-foreground mt-2">
          Requires active ball possession and multiple players visible.
        </div>
      </div>
    );
  }

  const latest = predictive[predictive.length - 1];
  const avgPass = (
    predictive.reduce((a: number, p: any) => a + p.pass_success, 0) / predictive.length
  ).toFixed(1);
  const avgLoss = (
    predictive.reduce((a: number, p: any) => a + p.loss_risk, 0) / predictive.length
  ).toFixed(1);
  const avgDanger = (
    predictive.reduce((a: number, p: any) => a + p.danger_prob, 0) / predictive.length
  ).toFixed(1);

  const getBarColor = (value: number, inverted = false) => {
    if (inverted) {
      return value > 70 ? "bg-red-500" : value > 40 ? "bg-yellow-500" : "bg-green-500";
    }
    return value > 70 ? "bg-green-500" : value > 40 ? "bg-yellow-500" : "bg-red-500";
  };

  return (
    <div className="grid gap-5 lg:grid-cols-3">
      {/* Pass Success */}
      <div className="glass rounded-2xl p-5">
        <div className="flex items-center gap-2 mb-4">
          <TrendingUp className="h-5 w-5 text-green-400" />
          <div className="text-xs uppercase tracking-wider text-muted-foreground">Pass Success</div>
        </div>
        <div className="font-display text-4xl font-bold text-green-400">
          {latest.pass_success.toFixed(1)}%
        </div>
        <div className="mt-3 h-2 overflow-hidden rounded-full bg-secondary">
          <div
            className={`h-full rounded-full ${getBarColor(latest.pass_success)}`}
            style={{ width: `${latest.pass_success}%` }}
          />
        </div>
        <div className="mt-3 text-xs text-muted-foreground">Avg across clip: {avgPass}%</div>
      </div>

      {/* Loss Risk */}
      <div className="glass rounded-2xl p-5">
        <div className="flex items-center gap-2 mb-4">
          <ShieldAlert className="h-5 w-5 text-red-400" />
          <div className="text-xs uppercase tracking-wider text-muted-foreground">
            Possession Loss Risk
          </div>
        </div>
        <div className="font-display text-4xl font-bold text-red-400">
          {latest.loss_risk.toFixed(1)}%
        </div>
        <div className="mt-3 h-2 overflow-hidden rounded-full bg-secondary">
          <div
            className={`h-full rounded-full ${getBarColor(latest.loss_risk, true)}`}
            style={{ width: `${latest.loss_risk}%` }}
          />
        </div>
        <div className="mt-3 text-xs text-muted-foreground">Avg across clip: {avgLoss}%</div>
      </div>

      {/* Danger Probability */}
      <div className="glass rounded-2xl p-5">
        <div className="flex items-center gap-2 mb-4">
          <Target className="h-5 w-5 text-yellow-400" />
          <div className="text-xs uppercase tracking-wider text-muted-foreground">Danger Phase</div>
        </div>
        <div className="font-display text-4xl font-bold text-yellow-400">
          {latest.danger_prob.toFixed(1)}%
        </div>
        <div className="mt-3 h-2 overflow-hidden rounded-full bg-secondary">
          <div
            className={`h-full rounded-full ${getBarColor(latest.danger_prob)}`}
            style={{ width: `${latest.danger_prob}%` }}
          />
        </div>
        <div className="mt-3 text-xs text-muted-foreground">Avg across clip: {avgDanger}%</div>
      </div>

      {/* Timeline */}
      <div className="glass col-span-full rounded-2xl p-5">
        <div className="mb-4 flex items-center gap-2">
          <Brain className="h-5 w-5 text-primary" />
          <div className="text-sm font-semibold">Predictive Timeline</div>
        </div>
        <div className="space-y-2 max-h-64 overflow-auto">
          {predictive.slice(-20).map((p: any, i: number) => {
            const seconds = Math.floor(p.frame / 30);
            const mm = String(Math.floor(seconds / 60)).padStart(2, "0");
            const ss = String(seconds % 60).padStart(2, "0");
            return (
              <div
                key={i}
                className="flex items-center gap-4 text-xs border-b border-border/30 pb-2"
              >
                <span className="font-mono text-muted-foreground w-12">
                  {mm}:{ss}
                </span>
                <span className="flex-1">
                  Pass:{" "}
                  <span className="font-semibold text-green-400">{p.pass_success.toFixed(0)}%</span>
                </span>
                <span className="flex-1">
                  Loss:{" "}
                  <span className="font-semibold text-red-400">{p.loss_risk.toFixed(0)}%</span>
                </span>
                <span className="flex-1">
                  Danger:{" "}
                  <span className="font-semibold text-yellow-400">{p.danger_prob.toFixed(0)}%</span>
                </span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
