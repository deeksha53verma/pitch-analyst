import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { toast } from "sonner";
import { HeaderHero } from "@/components/HeaderHero";
import { VideoComparisonSection } from "@/components/VideoComparisonSection";
import { SummaryMetrics } from "@/components/SummaryMetrics";
import { CVMetricsRow } from "@/components/CVMetricsRow";
import { TacticalTabs } from "@/components/TacticalTabs";
import { EventFeed } from "@/components/EventFeed";
import { LoadingAnalysisState } from "@/components/LoadingAnalysisState";
import { Toaster } from "@/components/ui/sonner";

export const Route = createFileRoute("/")({
  component: Dashboard,
  head: () => ({
    meta: [
      { title: "MatchMind — Football Tactical Intelligence Dashboard" },
      { name: "description", content: "AI-powered football match analysis: possession, build-up sequences, team compactness, player roles, and transition events." },
      { property: "og:title", content: "MatchMind — Football Tactical Intelligence" },
      { property: "og:description", content: "Upload a match clip and unlock tactical intelligence powered by computer vision." },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
});

function Dashboard() {
  const [fileName, setFileName] = useState<string | null>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [analyzed, setAnalyzed] = useState(false);

  const scrollToVideo = () => {
    document.getElementById("video-section")?.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  const handleUpload = () => {
    scrollToVideo();
    toast("Choose a football clip in the Original Video panel.");
  };

  const handleDemo = () => {
    setFileName("demo_match_liverpool_vs_arsenal.mp4");
    scrollToVideo();
    toast.success("Demo match loaded.");
  };

  const handleRun = () => {
    if (!fileName) setFileName("demo_match_liverpool_vs_arsenal.mp4");
    setAnalyzing(true);
  };

  return (
    <main className="min-h-screen">
      <HeaderHero onUpload={handleUpload} onDemo={handleDemo} onRun={handleRun} analyzed={analyzed} />

      <div id="video-section">
        <VideoComparisonSection fileName={fileName} onFile={setFileName} />
      </div>

      {analyzed && (
        <>
          <CVMetricsRow />
          <SummaryMetrics />
          <section className="mx-auto mt-10 max-w-7xl px-6">
            <div className="grid gap-5 lg:grid-cols-[1fr_320px]">
              <div><TacticalTabs /></div>
              <div className="lg:sticky lg:top-6 lg:self-start">
                <EventFeed />
              </div>
            </div>
          </section>
        </>
      )}

      <footer className="mx-auto mt-16 max-w-7xl px-6 py-8 text-center text-xs text-muted-foreground">
        MatchMind · Football Tactical Intelligence · Hackathon Demo
      </footer>

      {analyzing && (
        <LoadingAnalysisState
          onDone={() => {
            setAnalyzing(false);
            setAnalyzed(true);
            toast.success("Tactical analysis complete.");
          }}
        />
      )}
      <Toaster />
    </main>
  );
}
