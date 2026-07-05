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

import { useAnalysis } from "@/hooks/useAnalysis";

function Dashboard() {
  const [fileName, setFileName] = useState<string | null>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [analyzed, setAnalyzed] = useState(false);
  
  const { setData, resetData, setVideoUrls, selectedFile, setSelectedFile, setTimestamp } = useAnalysis();

  const scrollToVideo = () => {
    document.getElementById("video-section")?.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  const handleUpload = () => {
    scrollToVideo();
    toast("Choose a football clip in the Original Video panel.");
  };

  const handleDemo = () => {
    resetData();
    setFileName("demo_match_liverpool_vs_arsenal.mp4");
    setSelectedFile(null);
    setAnalyzed(false);
    scrollToVideo();
    toast.success("Demo match loaded.");
  };

  const handleFileSelect = (file: File) => {
    resetData();
    setSelectedFile(file);
    setFileName(file.name);
    setAnalyzed(false);
    scrollToVideo();
    toast.success(`Video file selected: ${file.name}`);
  };

  const handleReset = () => {
    resetData();
    setSelectedFile(null);
    setFileName(null);
    setAnalyzed(false);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleRun = () => {
    if (!selectedFile && !fileName) {
      setFileName("demo_match_liverpool_vs_arsenal.mp4");
    }
    
    setAnalyzing(true);
    
    if (selectedFile) {
      const formData = new FormData();
      formData.append("file", selectedFile);
      
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 120000); // 2-minute timeout
      
      const apiPromise = fetch("http://localhost:8000/api/analyze", {
        method: "POST",
        body: formData,
        signal: controller.signal,
      }).then(async (res) => {
        clearTimeout(timeoutId);
        if (!res.ok) throw new Error(`Server returned status: ${res.status}`);
        return res.json();
      }).catch((err) => {
        clearTimeout(timeoutId);
        if (err.name === "AbortError") {
          throw new Error("Request timed out (2 minutes limit). Please try a shorter video.");
        }
        throw err;
      });
      
      (window as any)._apiPromise = apiPromise;
    }
  };

  return (
    <main className="min-h-screen">
      <HeaderHero onUpload={handleUpload} onDemo={handleDemo} onRun={handleRun} onReset={handleReset} analyzed={analyzed} analyzing={analyzing} />

      <div id="video-section">
        <VideoComparisonSection fileName={fileName} onFile={handleFileSelect} />
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
          onDone={async () => {
            if (selectedFile) {
              try {
                const toastId = toast.loading("Finalizing tactical analysis...");
                const result = await (window as any)._apiPromise;
                if (result && result.status === "success") {
                  setData(result.data);
                  setVideoUrls(result.videos);
                  setTimestamp(Date.now());
                  setAnalyzing(false);
                  setAnalyzed(true);
                  toast.success("Tactical analysis complete.", { id: toastId });
                } else {
                  throw new Error("Analysis failed");
                }
              } catch (err: any) {
                console.error(err);
                setAnalyzing(false);
                toast.error(`Analysis failed: ${err.message}`);
              }
            } else {
              setAnalyzing(false);
              setAnalyzed(true);
              toast.success("Demo match tactical analysis complete.");
            }
          }}
        />
      )}
      <Toaster />
    </main>
  );
}
