import { players } from "@/data/mockData";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

export function PlayerRoleTab() {
  return (
    <div className="space-y-5">
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {players.map((p) => {
          const isBlue = p.team.includes("Blue");
          const c = isBlue ? "var(--team-blue)" : "var(--team-red)";
          return (
            <div key={`${p.team}-${p.num}`} className="glass rounded-2xl p-4">
              <div className="flex items-center gap-3">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl font-display text-lg font-bold text-white ring-2 ring-white/20" style={{ backgroundColor: `color-mix(in oklab, ${c} 85%, black)` }}>
                  #{p.num}
                </div>
                <div className="min-w-0">
                  <div className="truncate font-semibold">{p.role}</div>
                  <div className="text-xs text-muted-foreground">{p.team}</div>
                </div>
              </div>
              <div className="mt-4 space-y-1.5 text-xs">
                <div className="flex justify-between"><span className="text-muted-foreground">Dominant zone</span><span className="font-medium">{p.zone}</span></div>
                <div className="flex justify-between"><span className="text-muted-foreground">Touches</span><span className="font-mono">{p.touches}</span></div>
                <div className="flex justify-between"><span className="text-muted-foreground">Avg position</span><span className="font-mono">{p.avgPos}</span></div>
              </div>
            </div>
          );
        })}
      </div>

      <div className="glass rounded-2xl p-5">
        <div className="mb-3 text-sm font-semibold">Player Analytics Table</div>
        <Table>
          <TableHeader>
            <TableRow className="border-border hover:bg-transparent">
              <TableHead>Player</TableHead><TableHead>Team</TableHead><TableHead>Role</TableHead>
              <TableHead>Zone</TableHead><TableHead className="text-right">Touches</TableHead><TableHead>Avg Pos</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {players.map((p) => (
              <TableRow key={`${p.team}-${p.num}`} className="border-border">
                <TableCell className="font-semibold">#{p.num}</TableCell>
                <TableCell>
                  <Badge variant="outline" className={p.team.includes("Blue") ? "border-[color:var(--team-blue)]/40 text-[color:var(--team-blue)]" : "border-[color:var(--team-red)]/40 text-[color:var(--team-red)]"}>
                    {p.team}
                  </Badge>
                </TableCell>
                <TableCell>{p.role}</TableCell>
                <TableCell className="text-muted-foreground">{p.zone}</TableCell>
                <TableCell className="text-right font-mono">{p.touches}</TableCell>
                <TableCell className="font-mono text-muted-foreground">{p.avgPos}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
