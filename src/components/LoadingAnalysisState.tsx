import { analysisSteps } from "@/data/mockData";
import { Loader2, CheckCircle2, Circle } from "lucide-react";
import { useEffect, useState } from "react";
import { Progress } from "@/components/ui/progress";

export function LoadingAnalysisState({ onDone }: { onDone: () => void }) {
  const [step, setStep] = useState(0);
  useEffect(() => {
    const id = setInterval(() => {
      setStep((s) => {
        if (s >= analysisSteps.length - 1) {
          clearInterval(id);
          setTimeout(onDone, 700);
          return s;
        }
        return s + 1;
      });
    }, 550);
    return () => clearInterval(id);
  }, [onDone]);

  const progress = ((step + 1) / analysisSteps.length) * 100;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-background/80 p-6 backdrop-blur-md">
      <div className="glass w-full max-w-lg rounded-2xl p-8">
        <div className="mb-6 flex items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-gradient-to-br from-primary to-accent">
            <Loader2 className="h-5 w-5 animate-spin text-primary-foreground" />
          </div>
          <div>
            <div className="font-display text-lg font-semibold">Running Tactical Analysis</div>
            <div className="text-xs text-muted-foreground">MatchMind AI · vision + tracking pipeline</div>
          </div>
        </div>
        <Progress value={progress} className="mb-5 h-2" />
        <ul className="space-y-3 mt-4">
          {analysisSteps.map((s, i) => (
            <li key={s} className={`flex items-center gap-3 text-sm transition ${i < step ? "text-foreground" : i === step ? "text-primary font-medium" : "text-muted-foreground/50"}`}>
              {i < step ? (
                <CheckCircle2 className="h-4 w-4 text-primary" />
              ) : i === step ? (
                <Loader2 className="h-4 w-4 animate-spin text-primary" />
              ) : (
                <Circle className="h-4 w-4 text-muted-foreground/30" />
              )}
              {s}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
