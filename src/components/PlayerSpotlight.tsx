import { User, Activity, Map, ArrowRightLeft } from "lucide-react";
import { players } from "@/data/mockData";

export function PlayerSpotlight({ playerId = 10 }: { playerId?: number }) {
  const player = players.find(p => p.num === playerId) || players[0];
  
  return (
    <div className="glass rounded-2xl p-5 flex flex-col h-full">
      <div className="mb-4 flex items-center justify-between border-b border-border pb-3">
        <div className="flex items-center gap-3">
          <div className={`flex h-12 w-12 items-center justify-center rounded-full text-lg font-bold text-white shadow-lg ${player.team === "Team Blue" ? "bg-[color:var(--team-blue)] shadow-blue-500/20" : "bg-[color:var(--team-red)] shadow-red-500/20"}`}>
            {player.num}
          </div>
          <div>
            <div className="font-display font-bold text-lg">Player {player.num}</div>
            <div className="text-xs text-muted-foreground">{player.team} · {player.role}</div>
          </div>
        </div>
        <User className="h-5 w-5 text-muted-foreground/50" />
      </div>
      
      <div className="space-y-4 flex-1">
        <div>
          <div className="text-xs uppercase tracking-wider text-muted-foreground mb-1">Dominant Zone</div>
          <div className="flex items-center gap-2 font-medium">
            <Map className="h-4 w-4 text-primary" /> {player.zone}
          </div>
        </div>
        
        <div className="grid grid-cols-2 gap-3">
          <div className="rounded-lg bg-secondary/50 p-3">
            <div className="text-[10px] uppercase text-muted-foreground">Touches</div>
            <div className="text-lg font-bold tabular-nums">{player.touches}</div>
          </div>
          <div className="rounded-lg bg-secondary/50 p-3">
            <div className="text-[10px] uppercase text-muted-foreground">Involvements</div>
            <div className="text-lg font-bold tabular-nums">{Math.floor(player.touches * 0.4)}</div>
          </div>
        </div>
        
        <div>
          <div className="text-xs uppercase tracking-wider text-muted-foreground mb-2 mt-4">Sequence Involvements</div>
          <div className="space-y-2">
            <div className="flex items-center justify-between text-sm rounded-md bg-background/40 p-2">
              <span className="flex items-center gap-2"><Activity className="h-3.5 w-3.5 text-primary" /> Build-Ups</span>
              <span className="font-bold">{Math.floor(player.touches * 0.15)}</span>
            </div>
            <div className="flex items-center justify-between text-sm rounded-md bg-background/40 p-2">
              <span className="flex items-center gap-2"><ArrowRightLeft className="h-3.5 w-3.5 text-accent" /> Transitions</span>
              <span className="font-bold">{Math.floor(player.touches * 0.08)}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
