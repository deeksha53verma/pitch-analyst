import { feed } from "@/data/mockData";
import { Radio } from "lucide-react";

export function EventFeed() {
  return (
    <aside className="glass rounded-2xl p-4">
      <div className="mb-3 flex items-center justify-between">
        <div className="flex items-center gap-2 text-sm font-semibold">
          <Radio className="h-4 w-4 text-primary" /> Match Event Feed
        </div>
        <span className="flex items-center gap-1.5 text-xs text-primary">
          <span className="h-2 w-2 animate-pulse rounded-full bg-primary" /> live
        </span>
      </div>
      <ol className="relative space-y-3 border-l border-border pl-4">
        {feed.map((e, i) => (
          <li key={i} className="relative">
            <span className="absolute -left-[21px] top-1.5 h-2.5 w-2.5 rounded-full bg-primary ring-4 ring-primary/20" />
            <div className="text-[11px] font-mono uppercase tracking-wider text-muted-foreground">{e.t}</div>
            <div className="text-sm text-foreground">{e.text}</div>
          </li>
        ))}
      </ol>
    </aside>
  );
}
