export const teams = {
  blue: { name: "Team Blue", color: "team-blue" as const, possession: 58 },
  red: { name: "Team Red", color: "team-red" as const, possession: 42 },
};

export const summaryMetrics = [
  { label: "Team Blue Possession", value: "58%", icon: "circle-dot", tone: "blue" },
  { label: "Team Red Possession", value: "42%", icon: "circle-dot", tone: "red" },
  { label: "Build-Up Sequences", value: "14", icon: "route", tone: "primary" },
  { label: "Counterattack Events", value: "6", icon: "zap", tone: "accent" },
  { label: "Most Involved Player", value: "#10 Blue", icon: "user", tone: "blue" },
  { label: "Avg Team Compactness", value: "72%", icon: "target", tone: "primary" },
];

export const possessionTimeline = Array.from({ length: 24 }, (_, i) => ({
  minute: i * 4,
  blue: 40 + Math.round(20 * Math.sin(i / 3) + Math.random() * 8),
  red: 60 - Math.round(20 * Math.sin(i / 3) + Math.random() * 8),
}));

export const possessionEvents = [
  { time: "00:12", team: "Team Blue", player: "#10", event: "Ball Control" },
  { time: "00:16", team: "Team Blue", player: "#8", event: "Pass / Continuation" },
  { time: "00:20", team: "Team Red", player: "#6", event: "Turnover" },
  { time: "00:24", team: "Team Red", player: "#11", event: "Ball Carry" },
  { time: "00:29", team: "Team Blue", player: "#7", event: "Interception" },
  { time: "00:33", team: "Team Blue", player: "#10", event: "Progressive Pass" },
  { time: "00:38", team: "Team Red", player: "#9", event: "Turnover" },
  { time: "00:44", team: "Team Blue", player: "#8", event: "Ball Recovery" },
];

export const buildUps = [
  {
    id: "BU-01",
    start: "00:08",
    end: "00:19",
    team: "Team Blue",
    players: ["#3", "#6", "#8", "#10"],
    path: ["Own Third", "Middle Third", "Right Wing", "Final Third"],
    outcome: "Cross into box",
  },
  {
    id: "BU-02",
    start: "00:27",
    end: "00:36",
    team: "Team Red",
    players: ["#4", "#6", "#11"],
    path: ["Own Third", "Left Wing", "Middle Third"],
    outcome: "Turnover",
  },
  {
    id: "BU-03",
    start: "00:42",
    end: "00:58",
    team: "Team Blue",
    players: ["#5", "#8", "#10", "#7"],
    path: ["Middle Third", "Center", "Final Third", "Box Entry"],
    outcome: "Shot on target",
  },
  {
    id: "BU-04",
    start: "01:06",
    end: "01:14",
    team: "Team Red",
    players: ["#6", "#9", "#10"],
    path: ["Middle Third", "Right Half-Space", "Final Third"],
    outcome: "Blocked pass",
  },
];

export const compactness = {
  blue: { compactness: 74, width: 62, depth: 38, spread: 68 },
  red: { compactness: 69, width: 58, depth: 42, spread: 71 },
};

export const compactnessSeries = Array.from({ length: 20 }, (_, i) => ({
  minute: i * 5,
  blue: 60 + Math.round(15 * Math.sin(i / 2)),
  red: 55 + Math.round(15 * Math.cos(i / 2)),
}));

export const players = [
  { num: 10, team: "Team Blue", role: "Attacking Mid", zone: "Center / Final Third", touches: 64, avgPos: "72, 50" },
  { num: 8, team: "Team Blue", role: "Central Mid", zone: "Middle Third", touches: 58, avgPos: "55, 48" },
  { num: 7, team: "Team Blue", role: "Right Winger", zone: "Right Wing", touches: 41, avgPos: "68, 78" },
  { num: 3, team: "Team Blue", role: "Left Back", zone: "Left Half-Space", touches: 37, avgPos: "38, 22" },
  { num: 9, team: "Team Red", role: "Striker", zone: "Final Third", touches: 29, avgPos: "78, 50" },
  { num: 11, team: "Team Red", role: "Left Winger", zone: "Left Wing", touches: 44, avgPos: "62, 20" },
  { num: 6, team: "Team Red", role: "Defensive Mid", zone: "Middle Third", touches: 51, avgPos: "48, 52" },
  { num: 4, team: "Team Red", role: "Center Back", zone: "Own Third", touches: 39, avgPos: "28, 45" },
];

export const counterattacks = [
  { id: "T-01", time: "00:35–00:39", team: "Team Red", lane: "Left Wing", players: ["#11", "#9"], summary: "Fast break after turnover" },
  { id: "T-02", time: "01:12–01:17", team: "Team Blue", lane: "Center", players: ["#8", "#10", "#7"], summary: "Direct vertical transition" },
  { id: "T-03", time: "01:44–01:49", team: "Team Blue", lane: "Right Wing", players: ["#7", "#10"], summary: "Overlap and cross" },
  { id: "T-04", time: "02:03–02:08", team: "Team Red", lane: "Center", players: ["#6", "#9"], summary: "Counter through midfield" },
];

export const feed = [
  { t: "00:12", text: "Team Blue gained possession" },
  { t: "00:18", text: "Build-up sequence BU-01 started" },
  { t: "00:23", text: "Ball entered final third" },
  { t: "00:29", text: "#7 interception on right flank" },
  { t: "00:35", text: "Counterattack T-01 detected — Team Red" },
  { t: "00:44", text: "Ball recovery by #8" },
  { t: "00:58", text: "Shot on target — Team Blue" },
  { t: "01:12", text: "Counterattack T-02 detected — Team Blue" },
  { t: "01:22", text: "Compactness dropped for Team Red" },
  { t: "01:44", text: "Overlap on right — #7 delivers cross" },
];

export const analysisSteps = [
  "Video uploaded",
  "Frame extraction complete",
  "Player and ball detection complete",
  "Multi-object tracking complete",
  "Team classification complete",
  "Jersey OCR complete",
  "Possession engine complete",
  "Tactical event extraction complete",
];
