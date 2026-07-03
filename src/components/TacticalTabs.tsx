import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { PossessionTab } from "./tabs/PossessionTab";
import { BuildUpTab } from "./tabs/BuildUpTab";
import { CompactnessTab } from "./tabs/CompactnessTab";
import { PlayerRoleTab } from "./tabs/PlayerRoleTab";
import { CounterAttackTab } from "./tabs/CounterAttackTab";
import { CircleDot, Route, Grid3x3, Users, Zap } from "lucide-react";

export function TacticalTabs() {
  return (
    <section className="mx-auto mt-10 max-w-7xl px-6">
      <div className="mb-4">
        <h2 className="font-display text-2xl font-bold">Tactical Insights</h2>
        <p className="text-sm text-muted-foreground">Five AI-generated layers of match intelligence.</p>
      </div>
      <Tabs defaultValue="possession">
        <TabsList className="flex h-auto w-full flex-wrap justify-start gap-1 bg-secondary/50 p-1">
          <TabsTrigger value="possession" className="gap-1.5"><CircleDot className="h-3.5 w-3.5" /> Possession</TabsTrigger>
          <TabsTrigger value="buildup" className="gap-1.5"><Route className="h-3.5 w-3.5" /> Build-Up</TabsTrigger>
          <TabsTrigger value="compactness" className="gap-1.5"><Grid3x3 className="h-3.5 w-3.5" /> Team Shape</TabsTrigger>
          <TabsTrigger value="players" className="gap-1.5"><Users className="h-3.5 w-3.5" /> Player Roles</TabsTrigger>
          <TabsTrigger value="counter" className="gap-1.5"><Zap className="h-3.5 w-3.5" /> Transitions</TabsTrigger>
        </TabsList>
        <TabsContent value="possession" className="mt-5"><PossessionTab /></TabsContent>
        <TabsContent value="buildup" className="mt-5"><BuildUpTab /></TabsContent>
        <TabsContent value="compactness" className="mt-5"><CompactnessTab /></TabsContent>
        <TabsContent value="players" className="mt-5"><PlayerRoleTab /></TabsContent>
        <TabsContent value="counter" className="mt-5"><CounterAttackTab /></TabsContent>
      </Tabs>
    </section>
  );
}
