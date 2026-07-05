import { useAnalysis } from "@/hooks/useAnalysis";
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

export function PossessionTab() {
  const { data } = useAnalysis();
  const { teams, possessionTimeline, possessionEvents } = data;

  const totalPossessionEvents = possessionEvents.length;
  // The backend records states every 15 frames (0.5 seconds at 30fps)
  // Converting the state count to seconds of possession eliminates the 'ghost touches' confusion
  const blueSeconds = Math.round(((teams.blue as any).touches || 0) / 2);
  const redSeconds = Math.round(((teams.red as any).touches || 0) / 2);

  return (
    <div className="grid gap-5 lg:grid-cols-3">
      <div className="glass rounded-2xl p-5">
        <div className="text-xs uppercase tracking-wider text-muted-foreground">Team Blue Possession</div>
        <div className="mt-2 font-display text-4xl font-bold text-[color:var(--team-blue)]">{teams.blue.possession}%</div>
        <div className="mt-4 h-2 overflow-hidden rounded-full bg-secondary">
          <div className="h-full rounded-full bg-[color:var(--team-blue)]" style={{ width: `${teams.blue.possession}%` }} />
        </div>
        <div className="mt-4 text-sm text-muted-foreground">{totalPossessionEvents} changes · {blueSeconds}s possession</div>
      </div>
      <div className="glass rounded-2xl p-5">
        <div className="text-xs uppercase tracking-wider text-muted-foreground">Team Red Possession</div>
        <div className="mt-2 font-display text-4xl font-bold text-[color:var(--team-red)]">{teams.red.possession}%</div>
        <div className="mt-4 h-2 overflow-hidden rounded-full bg-secondary">
          <div className="h-full rounded-full bg-[color:var(--team-red)]" style={{ width: `${teams.red.possession}%` }} />
        </div>
        <div className="mt-4 text-sm text-muted-foreground">{totalPossessionEvents} changes · {redSeconds}s possession</div>
      </div>
      <div className="glass rounded-2xl p-5">
        <div className="text-xs uppercase tracking-wider text-muted-foreground">Ball Carrier Timeline</div>
        <div className="mt-3 flex h-8 w-full overflow-hidden rounded-lg">
          {possessionTimeline.map((p, i) => (
            <div key={i} className="h-full flex-1" style={{ backgroundColor: p.blue >= p.red ? "var(--team-blue)" : "var(--team-red)", opacity: 0.85 }} />
          ))}
        </div>
        <div className="mt-2 flex justify-between text-[10px] text-muted-foreground"><span>0'</span><span>45'</span><span>90'</span></div>
      </div>

      <div className="glass col-span-full rounded-2xl p-5">
        <div className="mb-3 flex items-center justify-between">
          <div className="text-sm font-semibold">Possession Over Time</div>
          <div className="flex items-center gap-4 text-xs text-muted-foreground">
            <span className="flex items-center gap-1.5"><span className="h-2 w-2 rounded-full bg-[color:var(--team-blue)]" /> Blue</span>
            <span className="flex items-center gap-1.5"><span className="h-2 w-2 rounded-full bg-[color:var(--team-red)]" /> Red</span>
          </div>
        </div>
        <div className="h-64 w-full">
          <ResponsiveContainer>
            <AreaChart data={possessionTimeline}>
              <defs>
                <linearGradient id="blueG" x1="0" x2="0" y1="0" y2="1">
                  <stop offset="0%" stopColor="oklch(0.68 0.19 245)" stopOpacity={0.6} />
                  <stop offset="100%" stopColor="oklch(0.68 0.19 245)" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="redG" x1="0" x2="0" y1="0" y2="1">
                  <stop offset="0%" stopColor="oklch(0.65 0.23 25)" stopOpacity={0.6} />
                  <stop offset="100%" stopColor="oklch(0.65 0.23 25)" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid stroke="oklch(1 0 0 / 0.06)" vertical={false} />
              <XAxis dataKey="minute" stroke="oklch(0.68 0.02 240)" fontSize={11} tickLine={false} axisLine={false} />
              <YAxis stroke="oklch(0.68 0.02 240)" fontSize={11} tickLine={false} axisLine={false} />
              <Tooltip contentStyle={{ background: "oklch(0.20 0.025 240)", border: "1px solid oklch(0.30 0.02 240)", borderRadius: 8, fontSize: 12 }} />
              <Area type="monotone" dataKey="blue" stroke="oklch(0.68 0.19 245)" fill="url(#blueG)" strokeWidth={2} />
              <Area type="monotone" dataKey="red" stroke="oklch(0.65 0.23 25)" fill="url(#redG)" strokeWidth={2} />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="glass col-span-full rounded-2xl p-5">
        <div className="mb-4 text-sm font-semibold">Possession Zones & Heatmap</div>
        <div className="pitch-bg relative h-64 w-full overflow-hidden rounded-xl border border-border flex items-center justify-center">
          {/* Mock Heatmap Blobs for Possession */}
          <div className="absolute h-40 w-40 rounded-full bg-[color:var(--team-blue)] blur-3xl opacity-30 top-1/4 left-1/4" />
          <div className="absolute h-48 w-48 rounded-full bg-[color:var(--team-blue)] blur-3xl opacity-40 bottom-1/4 left-1/3" />
          <div className="absolute h-32 w-32 rounded-full bg-[color:var(--team-blue)] blur-3xl opacity-20 top-1/2 left-2/3" />
          
          <div className="absolute h-32 w-32 rounded-full bg-[color:var(--team-red)] blur-3xl opacity-30 bottom-1/4 right-1/4" />
          <div className="absolute h-40 w-40 rounded-full bg-[color:var(--team-red)] blur-3xl opacity-20 top-1/3 right-1/3" />

          {/* Pitch lines */}
          <div className="absolute inset-0 pointer-events-none border-2 border-white/10 m-4 rounded-md flex">
            <div className="w-1/3 border-r-2 border-white/10 relative flex items-center">
              <div className="h-32 w-16 border-y-2 border-r-2 border-white/10 absolute left-0" />
            </div>
            <div className="w-1/3 border-r-2 border-white/10 relative" />
            <div className="w-1/3 relative flex items-center justify-end">
              <div className="h-32 w-16 border-y-2 border-l-2 border-white/10 absolute right-0" />
            </div>
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 h-24 w-24 rounded-full border-2 border-white/10" />
          </div>
        </div>
      </div>

      <div className="glass col-span-full rounded-2xl p-5">
        <div className="mb-3 text-sm font-semibold">Possession Events</div>
        <Table>
          <TableHeader>
            <TableRow className="border-border hover:bg-transparent">
              <TableHead>Time</TableHead><TableHead>Team</TableHead><TableHead>Player</TableHead><TableHead>Event</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {possessionEvents.map((e, i) => (
              <TableRow key={i} className="border-border">
                <TableCell className="font-mono text-xs text-muted-foreground">{e.time}</TableCell>
                <TableCell>
                  <Badge variant="outline" className={e.team.includes("Blue") ? "border-[color:var(--team-blue)]/40 text-[color:var(--team-blue)]" : "border-[color:var(--team-red)]/40 text-[color:var(--team-red)]"}>
                    {e.team}
                  </Badge>
                </TableCell>
                <TableCell className="font-semibold">{e.player}</TableCell>
                <TableCell className="text-muted-foreground">{e.event}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
