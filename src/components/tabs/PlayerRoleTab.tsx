import { useState } from "react";
import { useAnalysis } from "@/hooks/useAnalysis";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { PlayerSpotlight } from "../PlayerSpotlight";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

export function PlayerRoleTab() {
  const { data } = useAnalysis();
  const { players } = data;
  const firstNum = players.length > 0 ? players[0].num : 0;
  const [selectedPlayer, setSelectedPlayer] = useState(firstNum);

  const currentPlayerNum = players.find(p => p.num === selectedPlayer) ? selectedPlayer : firstNum;
  const player = players.find(p => p.num === currentPlayerNum) || players[0] || { num: 0, team: "", role: "", zone: "", touches: 0, avgPos: "0,0" };
  const isBlue = player.team.includes("Blue");
  const color = isBlue ? "var(--team-blue)" : "var(--team-red)";

  return (
    <div className="grid gap-5 lg:grid-cols-[1fr_320px]">
      <div className="space-y-5">
        <div className="flex items-center justify-between glass rounded-2xl p-4">
          <div className="text-sm font-semibold">Player Analysis</div>
          <Select value={selectedPlayer.toString()} onValueChange={(v) => setSelectedPlayer(parseInt(v))}>
            <SelectTrigger className="w-[180px] bg-secondary/50 border-none">
              <SelectValue placeholder="Select a player" />
            </SelectTrigger>
            <SelectContent>
              {players.map(p => (
                <SelectItem key={p.num} value={p.num.toString()}>
                  #{p.num} {p.team}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        {/* Heat Map Pitch */}
        <div className="glass rounded-2xl p-5">
          <div className="mb-4 text-sm font-semibold">Zone Occupation & Heat Map</div>
          <div className="pitch-bg relative h-64 w-full overflow-hidden rounded-xl border border-border flex items-center justify-center">
            {/* Mock heatmap blob based on dominant zone roughly */}
            <div 
              className="absolute h-32 w-48 rounded-full blur-3xl opacity-50"
              style={{
                backgroundColor: color,
                left: player.zone.includes("Right") ? "60%" : player.zone.includes("Left") ? "10%" : "35%",
                top: player.zone.includes("Third") ? "20%" : "40%",
              }} 
            />
            
            {/* Player marker */}
            <span className="absolute flex h-8 w-8 items-center justify-center rounded-full text-[12px] font-bold text-white shadow-[0_0_15px_rgba(0,0,0,0.5)] z-10"
              style={{
                backgroundColor: color,
                left: `calc(${player.avgPos.split(",")[0]}% - 16px)`,
                top: `calc(${player.avgPos.split(",")[1]}% - 16px)`,
              }}>
              {player.num}
            </span>

            {/* Pitch lines for decoration */}
            <div className="absolute inset-0 pointer-events-none border-2 border-white/10 m-4 rounded-md flex">
              <div className="w-1/2 border-r-2 border-white/10 relative flex items-center">
                <div className="h-32 w-16 border-y-2 border-r-2 border-white/10 absolute left-0" />
              </div>
              <div className="w-1/2 relative flex items-center justify-end">
                <div className="h-32 w-16 border-y-2 border-l-2 border-white/10 absolute right-0" />
              </div>
              <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 h-20 w-20 rounded-full border-2 border-white/10" />
            </div>
          </div>
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
                <TableRow 
                  key={`${p.team}-${p.num}`} 
                  className={`border-border cursor-pointer transition ${p.num === selectedPlayer ? "bg-primary/10" : "hover:bg-secondary/40"}`}
                  onClick={() => setSelectedPlayer(p.num)}
                >
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
      <div>
        <PlayerSpotlight playerId={selectedPlayer} />
      </div>
    </div>
  );
}
