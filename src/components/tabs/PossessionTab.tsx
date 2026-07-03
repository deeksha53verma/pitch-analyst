import { possessionTimeline, possessionEvents } from "@/data/mockData";
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

export function PossessionTab() {
  return (
    <div className="grid gap-5 lg:grid-cols-3">
      <div className="glass rounded-2xl p-5">
        <div className="text-xs uppercase tracking-wider text-muted-foreground">Team Blue Possession</div>
        <div className="mt-2 font-display text-4xl font-bold text-[color:var(--team-blue)]">58%</div>
        <div className="mt-4 h-2 overflow-hidden rounded-full bg-secondary">
          <div className="h-full rounded-full bg-[color:var(--team-blue)]" style={{ width: "58%" }} />
        </div>
        <div className="mt-4 text-sm text-muted-foreground">18 possession changes · 214 touches</div>
      </div>
      <div className="glass rounded-2xl p-5">
        <div className="text-xs uppercase tracking-wider text-muted-foreground">Team Red Possession</div>
        <div className="mt-2 font-display text-4xl font-bold text-[color:var(--team-red)]">42%</div>
        <div className="mt-4 h-2 overflow-hidden rounded-full bg-secondary">
          <div className="h-full rounded-full bg-[color:var(--team-red)]" style={{ width: "42%" }} />
        </div>
        <div className="mt-4 text-sm text-muted-foreground">18 possession changes · 168 touches</div>
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
