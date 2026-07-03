import { useState } from "react";
import { counterattacks } from "@/data/mockData";
import { Zap, ArrowRight, PlayCircle } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

export function CounterAttackTab() {
  const [selectedTransition, setSelectedTransition] = useState(counterattacks[0].id);

  const selected = counterattacks.find(c => c.id === selectedTransition) || counterattacks[0];
  const isBlue = selected.team.includes("Blue");
  const color = isBlue ? "var(--team-blue)" : "var(--team-red)";
  const strokeColor = isBlue ? "oklch(0.68 0.19 245)" : "oklch(0.65 0.23 25)";

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

      <div className="grid gap-5 lg:grid-cols-[1fr_320px]">
        <div className="space-y-5">
          <div className="glass rounded-2xl p-5 flex items-center justify-between">
            <div className="text-sm font-semibold">Transition Analysis</div>
            <Select value={selectedTransition} onValueChange={setSelectedTransition}>
              <SelectTrigger className="w-[180px] bg-secondary/50 border-none">
                <SelectValue placeholder="Select a transition" />
              </SelectTrigger>
              <SelectContent>
                {counterattacks.map(c => (
                  <SelectItem key={c.id} value={c.id}>
                    {c.id} ({c.team})
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="glass rounded-2xl p-5">
            <div className="mb-4 text-sm font-semibold">Counterattack Path</div>
            <div className="pitch-bg relative h-64 overflow-hidden rounded-xl border border-border flex items-center justify-center">
              {/* Pitch markings */}
              <div className="absolute inset-0 pointer-events-none border-2 border-white/10 m-4 rounded-md flex">
                <div className="w-1/2 border-r-2 border-white/10 relative flex items-center">
                  <div className="h-32 w-16 border-y-2 border-r-2 border-white/10 absolute left-0" />
                </div>
                <div className="w-1/2 relative flex items-center justify-end">
                  <div className="h-32 w-16 border-y-2 border-l-2 border-white/10 absolute right-0" />
                </div>
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 h-24 w-24 rounded-full border-2 border-white/10" />
              </div>
              
              {/* Draw path depending on selected */}
              <svg className="absolute inset-0 h-full w-full z-10" viewBox="0 0 100 100" preserveAspectRatio="none">
                <path 
                  d={selectedTransition === "T-01" ? "M 20,20 Q 50,20 80,40" : 
                     selectedTransition === "T-02" ? "M 30,50 L 85,50" :
                     selectedTransition === "T-03" ? "M 40,80 Q 70,80 90,50" :
                     "M 25,45 Q 50,60 85,55"} 
                  stroke={strokeColor} strokeWidth="1.5" strokeDasharray="3 2" fill="none" 
                />
                {/* Start point */}
                <circle cx={selectedTransition === "T-01" ? "20" : selectedTransition === "T-02" ? "30" : selectedTransition === "T-03" ? "40" : "25"} 
                        cy={selectedTransition === "T-01" ? "20" : selectedTransition === "T-02" ? "50" : selectedTransition === "T-03" ? "80" : "45"} 
                        r="2.5" fill={strokeColor} />
                {/* End point (arrow head style with circle) */}
                <circle cx={selectedTransition === "T-01" ? "80" : selectedTransition === "T-02" ? "85" : selectedTransition === "T-03" ? "90" : "85"} 
                        cy={selectedTransition === "T-01" ? "40" : selectedTransition === "T-02" ? "50" : selectedTransition === "T-03" ? "50" : "55"} 
                        r="3" fill="white" stroke={strokeColor} strokeWidth="1.5" />
              </svg>
            </div>
          </div>
        </div>
        
        <div className="flex flex-col gap-4">
          {counterattacks.map(c => {
            const cBlue = c.team.includes("Blue");
            return (
              <button 
                key={c.id} 
                onClick={() => setSelectedTransition(c.id)}
                className={`text-left transition rounded-2xl p-4 border ${selectedTransition === c.id ? "bg-secondary border-primary/30" : "glass hover:bg-secondary/40 border-transparent"}`}
              >
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <div className={`flex h-6 w-6 items-center justify-center rounded-md ${cBlue ? "bg-[color:var(--team-blue)]/15 text-[color:var(--team-blue)]" : "bg-[color:var(--team-red)]/15 text-[color:var(--team-red)]"}`}>
                      <Zap className="h-3 w-3" />
                    </div>
                    <div className="font-semibold">{c.id}</div>
                  </div>
                  <div className="text-[10px] text-muted-foreground">{c.time}</div>
                </div>
                <div className="text-sm font-medium" style={{ color: cBlue ? "var(--team-blue)" : "var(--team-red)" }}>{c.team}</div>
                <div className="text-xs mt-1 text-muted-foreground">{c.summary}</div>
              </button>
            )
          })}
        </div>
      </div>
    </div>
  );
}
