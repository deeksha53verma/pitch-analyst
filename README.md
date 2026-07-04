# MatchMind – Multi-Agent Tactical Intelligence for Football Video Analysis

MatchMind is a production-ready, AI-driven football video analysis project. It incorporates modern computer vision models (YOLO11, ByteTrack, etc.) to extract tactical intelligence, identify players, track the ball, and reconstruct the game state.

## Features (Planned)
- **Object Detection**: YOLO11 for player, referee, and ball detection.
- **Tracking**: ByteTrack integration for robust tracking across frames.
- **Jersey Number Recognition**: EasyOCR for robust ID extraction.
- **Pitch Segmentation**: Extracting pitch markings and keypoints.
- **Tactical Dashboard**: Streamlit interface linked with a React/Vite visualization frontend.

## Architecture & Configuration
This project utilizes [Hydra](https://hydra.cc/) for hierarchical configuration management. All configurations are stored in the `configs/` directory. 
The modular architecture ensures that data loading, training, and inference pipelines are fully isolated and robust.

## Setup Instructions

### Local Setup
1. Create a virtual environment (Python 3.11+).
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run tests to ensure everything is working:
   ```bash
   pytest tests/
   ```



## Modular Development
Development is separated into specific pipeline stages. The AI logic resides in `src/matchmind/`, and any UI/Visualization code resides in `frontend/`.

## Project Roadmap
The project is being strictly developed one module at a time.

### ✅ Finished Tasks
### ✅ Finished Tasks
- [x] **Module 0:** Environment Setup (PyTorch GPU, dependencies, dataset downloads)
- [x] **Module 1:** Project Structure & Configuration (Hydra, Loguru, pytest scaffolding)
- [x] **Module 2:** Dataset Manager (Validation & Loaders)
- [x] **Module 3:** Detection Module (YOLO11)
- [x] **Module 4:** Tracking Module (ByteTrack)
- [x] **Module 5:** Team Classification
- [x] **Module 6:** Jersey Number Recognition (EasyOCR)
- [x] **Module 7:** Player Identity Engine
- [x] **Module 8:** Pitch Mapping
- [x] **Module 9:** Ball Possession Engine
- [x] **Module 10:** Attack Build-up Detection
- [x] **Module 11:** Team Compactness Analysis
- [x] **Module 12:** Player Positional Analysis
- `[x]` Module 13: Counterattack Detection
- `[x]` Module 14: Visualization Engine
- `[x]` Module 15: Analytics Dashboard (Streamlit / React)
- `[x]` Module 16: Training Pipeline
- `[x]` Module 17: Evaluation Pipeline
- `[x]` Module 18: Final Integration

### ⏳ Remaining Tasks
All Modules Completed! 🚀

## Final Model Evaluation
The custom YOLO11 model achieved the following metrics on the hold-out validation dataset (Epoch 103/128):
- **Precision:** 91.1%
- **Recall:** 78.4%
- **mAP50:** 85.6%
- **mAP50-95:** 54.6%

### Per Class Accuracy
- **Players:** 94.7% Precision, 95.7% mAP50
- **Football:** 86.7% Precision, 75.2% mAP50

## License
MIT
