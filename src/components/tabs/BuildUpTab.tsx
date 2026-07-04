import { useState } from "react";
import { useAnalysis } from "@/hooks/useAnalysis";
import { ArrowRight, Users, PlayCircle } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

export function BuildUpTab() {
  const { data } = useAnalysis();
  const { buildUps } = data;
  const firstId = buildUps.length > 0 ? buildUps[0].id : "";
  const [selectedSequence, setSelectedSequence] = useState(firstId);

  const currentSequenceId = buildUps.find(b => b.id === selectedSequence) ? selectedSequence : firstId;
  const selected = buildUps.find(b => b.id === currentSequenceId) || buildUps[0] || { id: "", team: "", start: "", end: "", path: [], outcome: "", players: [] };
  const isBlue = selected.team.includes("Blue");
  const color = isBlue ? "oklch(0.68 0.19 245)" : "oklch(0.65 0.23 25)";
  const tailwindColor = isBlue ? "var(--team-blue)" : "var(--team-red)";

  return (
    <div className="grid gap-5 lg:grid-cols-[1fr_320px]">
      <div className="space-y-5">
        <div className="glass rounded-2xl p-5 flex items-center justify-between">
          <div className="text-sm font-semibold">Build-Up Sequence Viewer</div>
          <Select value={selectedSequence} onValueChange={setSelectedSequence}>
            <SelectTrigger className="w-[200px] bg-secondary/50 border-none">
              <SelectValue placeholder="Select a sequence" />
            </SelectTrigger>
            <SelectContent>
              {buildUps.map(b => (
                <SelectItem key={b.id} value={b.id}>
                  {b.id} ({b.team})
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="glass rounded-2xl p-5">
          <div className="mb-4 flex items-center justify-between">
            <div>
              <div className="text-xs font-mono uppercase text-muted-foreground">{selected.id} Details</div>
              <div className="font-display text-xl font-semibold mt-1">
                <span style={{ color: tailwindColor }}>{selected.team}</span> build-up
              </div>
            </div>
            <Badge variant="outline" className="font-mono text-xs gap-1">
              <PlayCircle className="h-3 w-3" /> {selected.start} → {selected.end}
            </Badge>
          </div>

          <div className="mb-4 flex flex-wrap items-center gap-1.5 text-sm font-medium">
            {selected.path.map((p, i) => (
              <span key={i} className="flex items-center gap-1.5">
                <span className="rounded-md bg-secondary/70 px-3 py-1.5">{p}</span>
                {i < selected.path.length - 1 && <ArrowRight className="h-4 w-4 text-muted-foreground" />}
              </span>
            ))}
          </div>
          
          <div className="flex items-center justify-between text-sm bg-background/50 p-3 rounded-xl border border-border/50">
            <div className="flex items-center gap-2">
              <Users className="h-4 w-4 text-muted-foreground" /> {selected.players.join(" · ")}
            </div>
            <span className="rounded-md bg-primary/15 px-2 py-1 font-semibold text-primary">{selected.outcome}</span>
          </div>
        </div>

        <div className="glass rounded-2xl p-5">
          <div className="mb-4 text-sm font-semibold">Progression Map</div>
          <div className="pitch-bg relative h-64 overflow-hidden rounded-xl border border-border flex items-center justify-center">
            {/* Simple mock pitch lines */}
            <div className="absolute inset-0 pointer-events-none border-2 border-white/10 m-4 rounded-md flex">
              <div className="w-1/3 border-r-2 border-white/10 relative" />
              <div className="w-1/3 border-r-2 border-white/10 relative" />
              <div className="w-1/3 relative" />
              <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 h-20 w-20 rounded-full border-2 border-white/10" />
            </div>

            {/* Sequence line drawing - randomized per sequence for mock visual */}
            <svg className="absolute inset-0 h-full w-full" viewBox="0 0 100 100" preserveAspectRatio="none">
              <path 
                d={selectedSequence === "BU-01" ? "M 20,80 Q 40,50 60,70 T 90,20" : 
                   selectedSequence === "BU-02" ? "M 15,30 Q 30,10 60,40" :
                   selectedSequence === "BU-03" ? "M 40,60 L 60,50 L 80,40 L 95,50" :
                   "M 45,80 Q 60,60 85,85"} 
                stroke={color} strokeWidth="1.5" strokeDasharray="3 2" fill="none" 
              />
              <circle cx={selectedSequence === "BU-01" ? "90" : selectedSequence === "BU-02" ? "60" : selectedSequence === "BU-03" ? "95" : "85"} 
                      cy={selectedSequence === "BU-01" ? "20" : selectedSequence === "BU-02" ? "40" : selectedSequence === "BU-03" ? "50" : "85"} 
                      r="2.5" fill="white" />
            </svg>
          </div>
        </div>
      </div>

      <div className="flex flex-col gap-4">
        {buildUps.map(b => (
          <button 
            key={b.id} 
            onClick={() => setSelectedSequence(b.id)}
            className={`text-left transition rounded-2xl p-4 border ${selectedSequence === b.id ? "bg-secondary border-primary/30" : "glass hover:bg-secondary/40 border-transparent"}`}
          >
            <div className="text-xs font-mono text-muted-foreground mb-1">{b.id}</div>
            <div className="font-semibold">{b.team}</div>
            <div className="text-xs mt-2 text-muted-foreground truncate">{b.path.join(" → ")}</div>
          </button>
        ))}
      </div>
    </div>
  );
}
