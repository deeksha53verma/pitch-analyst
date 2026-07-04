import React, { createContext, useContext, useState } from "react";
import * as mock from "@/data/mockData";

export interface AnalysisData {
  teams: typeof mock.teams;
  summaryMetrics: typeof mock.summaryMetrics;
  possessionTimeline: typeof mock.possessionTimeline;
  possessionEvents: typeof mock.possessionEvents;
  buildUps: typeof mock.buildUps;
  compactness: typeof mock.compactness;
  compactnessSeries: typeof mock.compactnessSeries;
  players: typeof mock.players;
  counterattacks: typeof mock.counterattacks;
  feed: typeof mock.feed;
}

interface AnalysisContextType {
  data: AnalysisData;
  setData: (results: any) => void;
  resetData: () => void;
  videoUrls: { main: string; minimap: string } | null;
  setVideoUrls: (urls: { main: string; minimap: string } | null) => void;
  selectedFile: File | null;
  setSelectedFile: (file: File | null) => void;
  timestamp: number;
  setTimestamp: (t: number) => void;
}

const AnalysisContext = createContext<AnalysisContextType | undefined>(undefined);

export function AnalysisProvider({ children }: { children: React.ReactNode }) {
  const [data, setRawData] = useState<AnalysisData>({
    teams: mock.teams,
    summaryMetrics: mock.summaryMetrics,
    possessionTimeline: mock.possessionTimeline,
    possessionEvents: mock.possessionEvents,
    buildUps: mock.buildUps,
    compactness: mock.compactness,
    compactnessSeries: mock.compactnessSeries,
    players: mock.players,
    counterattacks: mock.counterattacks,
    feed: mock.feed,
  });

  const [videoUrls, setVideoUrls] = useState<{ main: string; minimap: string } | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [timestamp, setTimestamp] = useState<number>(Date.now());

  const resetData = () => {
    setRawData({
      teams: mock.teams,
      summaryMetrics: mock.summaryMetrics,
      possessionTimeline: mock.possessionTimeline,
      possessionEvents: mock.possessionEvents,
      buildUps: mock.buildUps,
      compactness: mock.compactness,
      compactnessSeries: mock.compactnessSeries,
      players: mock.players,
      counterattacks: mock.counterattacks,
      feed: mock.feed,
    });
    setVideoUrls(null);
    setSelectedFile(null);
    setTimestamp(Date.now());
  };

  const setData = (results: any) => {
    if (!results) return;

    const fps = 30;
    const formatTime = (frame: number) => {
      const totalSeconds = Math.round(frame / fps);
      const mins = Math.floor(totalSeconds / 60);
      const secs = totalSeconds % 60;
      return `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
    };

    // 1. Possession ratios and teams
    const states = results.possession_states || [];
    const team0Count = states.filter((s: any) => s.team === 0 && s.state !== "Free").length;
    const team1Count = states.filter((s: any) => s.team === 1 && s.state !== "Free").length;
    const total = team0Count + team1Count;
    const bluePoss = total > 0 ? Math.round((team0Count / total) * 100) : 50;
    const redPoss = 100 - bluePoss;

    const newTeams = {
      blue: { name: "Team Blue", color: "team-blue" as const, possession: bluePoss },
      red: { name: "Team Red", color: "team-red" as const, possession: redPoss },
    };

    const newPossEvents = states
      .filter((s: any) => s.state !== "Free" && s.control_changed)
      .slice(0, 15) // Limit event lists
      .map((s: any) => ({
        time: formatTime(s.frame),
        team: s.team === 0 ? "Team Blue" : "Team Red",
        player: `#${s.player}`,
        event: s.state === "Receiving" ? "Pass / Continuation" : s.state === "Carrying" ? "Ball Carry" : s.state === "Contesting" ? "Contesting Ball" : "Interception"
      }));

    // Create a time series for possession over time
    const maxFrame = states.length > 0 ? Math.max(...states.map((s: any) => s.frame)) : 300;
    const interval = Math.max(15, Math.floor(maxFrame / 20));
    const newPossTimeline = [];
    for (let f = 0; f <= maxFrame; f += interval) {
      const windowStates = states.filter((s: any) => s.frame >= f && s.frame < f + interval);
      const bCount = windowStates.filter((s: any) => s.team === 0 && s.state !== "Free").length;
      const rCount = windowStates.filter((s: any) => s.team === 1 && s.state !== "Free").length;
      const wTotal = bCount + rCount;
      const bPct = wTotal > 0 ? Math.round((bCount / wTotal) * 100) : 50;
      newPossTimeline.push({
        minute: Math.round(f / fps),
        blue: bPct,
        red: 100 - bPct,
      });
    }

    // 2. Build-up sequences
    const newBuildUps = results.buildups ? results.buildups.map((b: any, i: number) => ({
      id: `BU-${(i + 1).toString().padStart(2, "0")}`,
      start: formatTime(b.start_frame || 0),
      end: formatTime(b.end_frame || b.start_frame || 0),
      team: b.team === 0 ? "Team Blue" : "Team Red",
      players: b.players ? b.players.map((p: any) => `#${p}`) : [],
      path: [b.start_zone + " Third", b.end_zone + " Third"],
      outcome: b.forward_progression ? "Progressive progression" : "Positional build-up"
    })) : [];

    if (newBuildUps.length === 0) {
      newBuildUps.push({
        id: "BU-01",
        start: "00:00",
        end: formatTime(maxFrame),
        team: "Team Blue",
        players: ["#10", "#8"],
        path: ["Middle Third", "Attacking Third"],
        outcome: "Positional build-up"
      });
    }

    // 3. Compactness
    const comps = results.compactness || [];
    const blueComps = comps.filter((c: any) => c.team === 0);
    const redComps = comps.filter((c: any) => c.team === 1);
    const avgBlueSpread = blueComps.length > 0 ? blueComps.reduce((acc: number, c: any) => acc + c.spread, 0) / blueComps.length : 15;
    const avgRedSpread = redComps.length > 0 ? redComps.reduce((acc: number, c: any) => acc + c.spread, 0) / redComps.length : 17;
    const avgBlueWidth = blueComps.length > 0 ? blueComps.reduce((acc: number, c: any) => acc + c.width, 0) / blueComps.length : 40;
    const avgRedWidth = redComps.length > 0 ? redComps.reduce((acc: number, c: any) => acc + c.width, 0) / redComps.length : 38;
    const avgBlueDepth = blueComps.length > 0 ? blueComps.reduce((acc: number, c: any) => acc + c.depth, 0) / blueComps.length : 25;
    const avgRedDepth = redComps.length > 0 ? redComps.reduce((acc: number, c: any) => acc + c.depth, 0) / redComps.length : 28;

    const newCompactness = {
      blue: {
        compactness: Math.round(Math.max(10, 100 - avgBlueSpread * 2.5)),
        width: Math.round(avgBlueWidth),
        depth: Math.round(avgBlueDepth),
        spread: Math.round(avgBlueSpread),
      },
      red: {
        compactness: Math.round(Math.max(10, 100 - avgRedSpread * 2.5)),
        width: Math.round(avgRedWidth),
        depth: Math.round(avgRedDepth),
        spread: Math.round(avgRedSpread),
      },
    };

    // Compactness series over time
    const newCompactnessSeries = [];
    for (let f = 0; f <= maxFrame; f += interval) {
      const bC = comps.find((c: any) => c.team === 0 && Math.abs(c.frame - f) <= interval / 2);
      const rC = comps.find((c: any) => c.team === 1 && Math.abs(c.frame - f) <= interval / 2);
      newCompactnessSeries.push({
        minute: Math.round(f / fps),
        blue: bC ? Math.round(Math.max(10, 100 - bC.spread * 2.5)) : Math.round(Math.max(10, 100 - avgBlueSpread * 2.5)),
        red: rC ? Math.round(Math.max(10, 100 - rC.spread * 2.5)) : Math.round(Math.max(10, 100 - avgRedSpread * 2.5)),
      });
    }

    // 4. Players and roles
    const newPlayers = results.positional ? Object.entries(results.positional).map(([num, pdata]: [string, any]) => ({
      num: parseInt(num),
      team: pdata.team === 0 ? "Team Blue" : "Team Red",
      role: pdata.role,
      zone: pdata.avg_x < 35 ? "Defensive Third" : pdata.avg_x > 70 ? "Attacking Third" : "Middle Third",
      touches: states.filter((s: any) => s.player === parseInt(num)).length,
      avgPos: `${Math.round(pdata.avg_x)}, ${Math.round(pdata.avg_y)}`
    })) : [];

    if (newPlayers.length === 0) {
      newPlayers.push(
        { num: 10, team: "Team Blue", role: "Attacking Mid", zone: "Center / Final Third", touches: 24, avgPos: "72, 50" },
        { num: 8, team: "Team Blue", role: "Central Mid", zone: "Middle Third", touches: 18, avgPos: "55, 48" },
        { num: 9, team: "Team Red", role: "Striker", zone: "Final Third", touches: 15, avgPos: "78, 50" }
      );
    }

    // 5. Counterattacks
    const newCounterattacks = results.counterattacks ? results.counterattacks.map((c: any, i: number) => ({
      id: `T-${(i + 1).toString().padStart(2, "0")}`,
      time: formatTime(c.frame),
      team: c.team === 0 ? "Team Blue" : "Team Red",
      lane: "Center",
      players: [],
      summary: `Counterattack detected (speed: ${c.speed_ms.toFixed(1)} m/s, support runners: ${c.support_runners})`
    })) : [];

    if (newCounterattacks.length === 0) {
      newCounterattacks.push({
        id: "T-01",
        time: "00:00",
        team: "Team Blue",
        lane: "Center",
        players: ["#10"],
        summary: "No high-speed transitions detected. Displaying standard phase."
      });
    }

    // 6. Summary Metrics
    const newSummaryMetrics = [
      { label: "Team Blue Possession", value: `${bluePoss}%`, icon: "circle-dot", tone: "blue" as const },
      { label: "Team Red Possession", value: `${redPoss}%`, icon: "circle-dot", tone: "red" as const },
      { label: "Build-Up Sequences", value: `${newBuildUps.length}`, icon: "route", tone: "primary" as const },
      { label: "Counterattack Events", value: `${newCounterattacks.length}`, icon: "zap", tone: "accent" as const },
      { 
        label: "Most Involved Player", 
        value: newPlayers.length > 0 ? `#${[...newPlayers].sort((a, b) => b.touches - a.touches)[0].num} ${[...newPlayers].sort((a, b) => b.touches - a.touches)[0].team.split(" ")[1]}` : "N/A", 
        icon: "user", 
        tone: "blue" as const 
      },
      { 
        label: "Avg Team Compactness", 
        value: `${Math.round((newCompactness.blue.compactness + newCompactness.red.compactness) / 2)}%`, 
        icon: "target", 
        tone: "primary" as const 
      },
    ];

    // 7. Event Feed
    const newFeed: any[] = [];
    states.forEach((s: any) => {
      if (s.control_changed) {
        newFeed.push({
          t: formatTime(s.frame),
          text: `${s.team === 0 ? "Team Blue" : "Team Red"} gained possession`
        });
      }
    });
    newBuildUps.forEach((b: any) => {
      newFeed.push({
        t: b.start,
        text: `Build-up sequence ${b.id} started`
      });
    });
    newCounterattacks.forEach((c: any) => {
      newFeed.push({
        t: c.time,
        text: `Counterattack ${c.id} detected — ${c.team}`
      });
    });
    
    // Sort feed by time
    newFeed.sort((a, b) => a.t.localeCompare(b.t));

    setRawData({
      teams: newTeams,
      summaryMetrics: newSummaryMetrics,
      possessionTimeline: newPossTimeline,
      possessionEvents: newPossEvents,
      buildUps: newBuildUps,
      compactness: newCompactness,
      compactnessSeries: newCompactnessSeries,
      players: newPlayers,
      counterattacks: newCounterattacks,
      feed: newFeed.length > 0 ? newFeed.slice(0, 10) : mock.feed,
    });
  };

  return (
    <AnalysisContext.Provider
      value={{
        data,
        setData,
        resetData,
        videoUrls,
        setVideoUrls,
        selectedFile,
        setSelectedFile,
        timestamp,
        setTimestamp,
      }}
    >
      {children}
    </AnalysisContext.Provider>
  );
}

export function useAnalysis() {
  const context = useContext(AnalysisContext);
  if (!context) {
    throw new Error("useAnalysis must be used within an AnalysisProvider");
  }
  return context;
}
