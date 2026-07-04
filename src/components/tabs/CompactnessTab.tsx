import { useAnalysis } from "@/hooks/useAnalysis";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";

function TeamCard({ team, data, color }: { team: string; data: { compactness: number; width: number; depth: number; spread: number }; color: string }) {
  const stats = [
    { label: "Compactness", value: data.compactness },
    { label: "Width", value: data.width },
    { label: "Depth", value: data.depth },
    { label: "Spread", value: data.spread },
  ];
  
  // Create a polygon based on mock formation points
  const points = team.includes("Blue") ? 
    [[50, 90], [20, 70], [40, 70], [60, 70], [80, 70], [30, 45], [50, 45], [70, 45], [35, 22], [65, 22], [50, 10]] :
    [[50, 10], [20, 30], [40, 30], [60, 30], [80, 30], [30, 55], [50, 55], [70, 55], [35, 78], [65, 78], [50, 90]];
  
  const hullPoints = team.includes("Blue") ? "20,70 35,22 50,10 65,22 80,70 50,90" : "20,30 35,78 50,90 65,78 80,30 50,10";

  return (
    <div className="glass rounded-2xl p-5 flex flex-col h-full">
      <div className="mb-4 flex items-center justify-between">
        <div className="font-display text-lg font-semibold" style={{ color }}>{team}</div>
        <div className="text-xs text-muted-foreground">shape metrics</div>
      </div>
      <div className="mb-4 grid grid-cols-2 gap-3">
        {stats.map((s) => (
          <div key={s.label} className="rounded-lg bg-secondary/60 p-3">
            <div className="text-[10px] uppercase tracking-wider text-muted-foreground">{s.label}</div>
            <div className="mt-1 flex items-baseline gap-1">
              <span className="font-display text-2xl font-bold tabular-nums">{s.value}</span>
              <span className="text-xs text-muted-foreground">%</span>
            </div>
            <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-background">
              <div className="h-full" style={{ width: `${s.value}%`, backgroundColor: color }} />
            </div>
          </div>
        ))}
      </div>
      <div className="flex-1 mt-2">
        <div className="text-xs font-semibold mb-3">Average Team Shape</div>
        <div className="pitch-bg relative h-64 overflow-hidden rounded-lg border border-border">
          {/* Pitch markings */}
          <div className="absolute inset-0 border-2 border-white/10 m-2 rounded flex">
            <div className="w-1/2 border-r-2 border-white/10 relative" />
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 h-16 w-16 rounded-full border-2 border-white/10" />
          </div>
          
          <svg className="absolute inset-0 h-full w-full" viewBox="0 0 100 100" preserveAspectRatio="none">
            <polygon points={hullPoints} fill={color} fillOpacity="0.2" stroke={color} strokeWidth="1" strokeDasharray="2 1" />
          </svg>
          
          {points.map(([x, y], i) => (
            <span key={i} className="absolute h-3 w-3 -translate-x-1/2 -translate-y-1/2 rounded-full ring-2 ring-white/40 shadow-lg" style={{ left: `${x}%`, top: `${y}%`, backgroundColor: color }} />
          ))}
        </div>
      </div>
    </div>
  );
}

export function CompactnessTab() {
  const { data } = useAnalysis();
  const { compactness, compactnessSeries } = data;
  return (
    <div className="grid gap-5 lg:grid-cols-2">
      <TeamCard team="Team Blue" data={compactness.blue} color="oklch(0.68 0.19 245)" />
      <TeamCard team="Team Red" data={compactness.red} color="oklch(0.65 0.23 25)" />
      <div className="glass col-span-full rounded-2xl p-5">
        <div className="mb-3 flex items-center justify-between">
          <div className="text-sm font-semibold">Compactness Over Time</div>
          <div className="flex items-center gap-4 text-xs text-muted-foreground">
            <span className="flex items-center gap-1.5"><span className="h-2 w-2 rounded-full bg-[color:var(--team-blue)]" /> Blue</span>
            <span className="flex items-center gap-1.5"><span className="h-2 w-2 rounded-full bg-[color:var(--team-red)]" /> Red</span>
          </div>
        </div>
        <div className="h-56">
          <ResponsiveContainer>
            <LineChart data={compactnessSeries}>
              <CartesianGrid stroke="oklch(1 0 0 / 0.06)" vertical={false} />
              <XAxis dataKey="minute" stroke="oklch(0.68 0.02 240)" fontSize={11} tickLine={false} axisLine={false} />
              <YAxis stroke="oklch(0.68 0.02 240)" fontSize={11} tickLine={false} axisLine={false} />
              <Tooltip contentStyle={{ background: "oklch(0.20 0.025 240)", border: "1px solid oklch(0.30 0.02 240)", borderRadius: 8, fontSize: 12 }} />
              <Line type="monotone" dataKey="blue" stroke="oklch(0.68 0.19 245)" strokeWidth={2.5} dot={false} />
              <Line type="monotone" dataKey="red" stroke="oklch(0.65 0.23 25)" strokeWidth={2.5} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
