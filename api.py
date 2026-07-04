import os
import shutil
import json
from pathlib import Path
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import sys
sys.path.append(os.path.abspath("src"))

from matchmind.core.config import load_config # type: ignore
from matchmind.pipeline.runner import PipelineRunner # type: ignore

app = FastAPI(title="MatchMind Backend API")

# Enable CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the output directory as static files so frontend can stream videos
out_dir = Path("outputs/dashboard")
out_dir.mkdir(parents=True, exist_ok=True)
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

# Initialize Runner globally
cfg = load_config(config_name="main")
runner = PipelineRunner(cfg)

@app.post("/api/analyze")
async def analyze_video(file: UploadFile = File(...)):
    # Save the uploaded video to a temp file
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        # Run the MatchMind pipeline
        out_video, minimap_video = runner.run(temp_path, out_dir="outputs/dashboard")
        
        # Load the generated JSON data to return to the frontend
        results = {}
        json_files = [
            "buildups.json", "compactness.json", "counterattacks.json", 
            "positional.json", "possession_states.json", "predictive.json"
        ]
        
        for json_file in json_files:
            file_path = out_dir / json_file
            if file_path.exists():
                with open(file_path, "r") as f:
                    try:
                        results[json_file.replace(".json", "")] = json.load(f)
                    except json.JSONDecodeError:
                        results[json_file.replace(".json", "")] = None
            else:
                results[json_file.replace(".json", "")] = None
                
        return {
            "status": "success",
            "videos": {
                "main": f"/outputs/dashboard/output_h264.mp4",
                "minimap": f"/outputs/dashboard/minimap_h264.mp4"
            },
            "data": results
        }
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.get("/api/results")
def get_results():
    results = {}
    json_files = [
        "buildups.json", "compactness.json", "counterattacks.json", 
        "positional.json", "possession_states.json", "predictive.json"
    ]
    
    for json_file in json_files:
        file_path = out_dir / json_file
        if file_path.exists():
            with open(file_path, "r") as f:
                try:
                    results[json_file.replace(".json", "")] = json.load(f)
                except json.JSONDecodeError:
                    results[json_file.replace(".json", "")] = None
        else:
            results[json_file.replace(".json", "")] = None
            
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
