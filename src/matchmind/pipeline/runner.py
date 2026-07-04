import sys
import os
import json
import numpy as np
from pathlib import Path
from matchmind.core.logger import logger

from matchmind.tactics.buildup import BuildUpEngine # type: ignore
from matchmind.tactics.compactness import CompactnessEngine # type: ignore
from matchmind.tactics.positional import PositionalEngine # type: ignore
from matchmind.tactics.counterattack import CounterattackEngine # type: ignore
from matchmind.possession.state_engine import PossessionStateEngine # type: ignore
from matchmind.tactics.predictive import PredictiveEngine # type: ignore
import types

# Create a mock config for visualizer
cfg = types.SimpleNamespace()
cfg.mapping = types.SimpleNamespace()
cfg.mapping.params = {"pitch_length": 105.0, "pitch_width": 68.0, "scale_factor": 10.0}
from matchmind.mapping.visualizer import PitchVisualizer # type: ignore

class PipelineRunner:
    def __init__(self, config=None):
        self.config = config
        
        # Initialize AI Tactical Engines
        logger.info("Loading Tactical Engines...")
        pitch_cfg = {"thirds": {"defensive": 35.0, "middle": 70.0, "attacking": 105.0}, 
                     "channels": {"left": 22.6, "center": 45.3, "right": 68.0}}
                     
        self.buildup = BuildUpEngine(pitch_cfg["thirds"])
        self.compactness = CompactnessEngine()
        self.positional = PositionalEngine(pitch_cfg)
        self.counterattack = CounterattackEngine(speed_threshold=5.0)
        self.state_engine = PossessionStateEngine()
        self.predictive = PredictiveEngine()

    def run(self, video_path, out_dir="outputs/dashboard"):
        """Run the actual Computer Vision and Tactical Pipeline on a video."""
        import cv2
        from ultralytics import YOLO
        
        # Reset tracker state
        self.ball_px_ema = None
        self.ball_py_ema = None
        
        logger.info(f"Initializing YOLO with best.pt weights...")
        weights_path = Path("runs/detect/runs/train/matchmind_yolo/weights/best.pt")
        
        if not weights_path.exists():
            logger.error("best.pt not found! Please train the model first.")
            return False
            
        model = YOLO(weights_path)
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            logger.error("Could not open video file.")
            return False

        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Scale down 4K to 1080p to prevent OpenCV Writer crashes and VRAM OOM
        if width > 1920:
            scale = 1920 / width
            width = 1920
            height = int(height * scale)
        
        # Output writers
        os.makedirs(out_dir, exist_ok=True)
        out_video_path = str(Path(out_dir) / "output.mp4")
        minimap_path = str(Path(out_dir) / "minimap.mp4")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Using mp4v as fallback for Windows OpenCV
        out = cv2.VideoWriter(out_video_path, fourcc, fps, (width, height))
        
        # Minimap is always 1050x680 based on PitchVisualizer
        visualizer = PitchVisualizer(cfg)
        mini_out = cv2.VideoWriter(minimap_path, fourcc, fps, (visualizer.w_px, visualizer.h_px))
        
        if not out.isOpened():
            logger.error(f"Failed to initialize VideoWriter for dimensions {width}x{height}")
            cap.release()
            return False

        logger.info("Starting frame-by-frame tracking and tactical analysis...")
        
        frame_idx = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            frame_idx += 1
            # Resize frame if it was scaled down
            if frame.shape[1] > 1920:
                frame = cv2.resize(frame, (width, height))
                
            # Run YOLO Tracking (lowered conf for amateur wide-angle footage)
            results = model.track(frame, persist=True, verbose=False, conf=0.15)
            
            # Extract player coordinates
            team_0_points = []
            team_1_points = []
            player_data = {}
            
            if results and len(results) > 0 and results[0].boxes is not None:
                res = results[0]
                annotated_frame = res.plot() # Draw YOLO boxes automatically
                
                boxes = res.boxes
                players_pitch = []
                ball_pitch = None
                closest_player_dist = float('inf')
                possessing_team = -1
                possessing_player = -1
                
                if boxes is not None:
                    # Fallback to pseudo-IDs if tracker fails to assign IDs
                    ids = boxes.id.cpu().numpy().astype(int) if boxes.id is not None else np.arange(len(boxes))
                    cls = boxes.cls.cpu().numpy().astype(int)
                    xyxy = boxes.xyxy.cpu().numpy()
                    
                    # Find the best ball in this frame (highest confidence)
                    best_ball = None
                    best_ball_conf = -1
                    
                    for i, box_id in enumerate(ids):
                        box_id = int(box_id)
                        class_id = int(cls[i])
                        conf = float(boxes.conf[i].cpu().numpy()) if hasattr(boxes, 'conf') and boxes.conf is not None else 1.0
                        
                        x1, y1, x2, y2 = xyxy[i]
                        cx = (x1 + x2) / 2.0
                        
                        # Anchor players to their feet (y2), ball to center
                        if class_id == 0:
                            cy = y2
                        else:
                            cy = (y1 + y2) / 2.0
                        
                        # Pseudo-linear mapping to physical pitch (0 to 105, 0 to 68)
                        px = (cx / width) * 105.0
                        py = (cy / height) * 68.0
                        
                        if class_id == 0: # Player
                            team_id = box_id % 2 
                            if team_id == 0:
                                team_0_points.append([cx, cy])
                            else:
                                team_1_points.append([cx, cy])
                                
                            player_data[box_id] = {"team": team_id, "x": px, "y": py}
                            players_pitch.append((px, py, team_id))
                            self.positional.update(box_id, team_id, px, py)
                            
                        elif class_id == 1: # Ball
                            if conf > best_ball_conf:
                                best_ball_conf = conf
                                best_ball = (px, py)
                    
                    if best_ball:
                        px, py = best_ball
                        # Apply Exponential Moving Average (EMA) smoothing to stabilize ball
                        if not hasattr(self, 'ball_px_ema') or self.ball_px_ema is None:
                            self.ball_px_ema = px
                            self.ball_py_ema = py
                        else:
                            alpha = 0.15 # Stronger smoothing factor
                            self.ball_px_ema = alpha * px + (1 - alpha) * self.ball_px_ema
                            self.ball_py_ema = alpha * py + (1 - alpha) * self.ball_py_ema
                        
                        ball_pitch = (self.ball_px_ema, self.ball_py_ema)
                            
                # Determine Possession for BuildUp
                if ball_pitch:
                    for pid, pdata in player_data.items():
                        dist = ((pdata["x"] - ball_pitch[0])**2 + (pdata["y"] - ball_pitch[1])**2)**0.5
                        if dist < closest_player_dist:
                            closest_player_dist = dist
                            possessing_team = pdata["team"]
                            possessing_player = pid
                            
                    if possessing_team != -1:
                        self.buildup.update(frame_idx, possessing_team, possessing_player, ball_pitch[0])
                        
                # Update Match Understanding & Predictive Layers
                self.state_engine.update(frame_idx, player_data, ball_pitch)
                self.predictive.predict(frame_idx, self.state_engine, player_data, ball_pitch)
                            
                # Tactical Engines Step
                if len(team_0_points) > 2:
                    self.compactness.calculate_frame(frame_idx, 0, team_0_points)
                if len(team_1_points) > 2:
                    self.compactness.calculate_frame(frame_idx, 1, team_1_points)
                    
                self.counterattack.update(frame_idx, 0, 10.0, player_data, fps)
                
                # Write frames
                out.write(annotated_frame)
                canvas = visualizer.draw_pitch()
                canvas = visualizer.plot_entities(canvas, players_pitch, ball_pitch)
                mini_out.write(canvas)
            else:
                out.write(frame)
                canvas = visualizer.draw_pitch()
                mini_out.write(canvas)
                
        cap.release()
        out.release()
        mini_out.release()
        
        logger.info("Exporting Tactical Data for Streamlit Dashboard...")
        self.buildup.export(out_dir)
        self.compactness.export(out_dir)
        self.positional.export(out_dir)
        self.counterattack.export(out_dir)
        self.state_engine.export(out_dir)
        self.predictive.export(out_dir)
        
        logger.info(f"Video saved to {out_video_path}")
        
        # Transcode to H.264 for browser compatibility
        h264_out = str(Path(out_dir) / "output_h264.mp4")
        h264_mini = str(Path(out_dir) / "minimap_h264.mp4")
        
        try:
            import imageio_ffmpeg
            import subprocess
            ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
            
            logger.info("Transcoding to H.264 for browser compatibility...")
            r1 = subprocess.run([ffmpeg_exe, "-i", out_video_path, "-vcodec", "libx264", "-pix_fmt", "yuv420p", "-movflags", "faststart", "-y", h264_out], capture_output=True, text=True)
            r2 = subprocess.run([ffmpeg_exe, "-i", minimap_path, "-vcodec", "libx264", "-pix_fmt", "yuv420p", "-movflags", "faststart", "-y", h264_mini], capture_output=True, text=True)
            
            if r1.returncode == 0 and r2.returncode == 0:
                logger.info("H.264 transcode successful!")
                return h264_out, h264_mini
            else:
                logger.warning(f"FFmpeg transcode failed, serving raw files. stderr: {r1.stderr[:200]}")
        except Exception as e:
            logger.warning(f"FFmpeg transcode error: {e}. Serving raw files instead.")
        
        # Fallback: copy raw files with h264 names so frontend URLs still work
        import shutil
        shutil.copy2(out_video_path, h264_out)
        shutil.copy2(minimap_path, h264_mini)
        return h264_out, h264_mini
        
    def execute_dummy_run(self, out_dir="outputs/dashboard"):
        """For the Dashboard demo, we simulate a mock run to generate some data."""
        logger.info("Simulating full match analysis pipeline...")
        
        self.compactness.calculate_frame(1, 0, [[10, 20], [15, 30], [20, 25]])
        self.positional.update(10, 0, 80.0, 34.0)
        self.counterattack.update(1, 1, 10.0, {99: {"team": 1, "x": 80.0}}, fps=30)
        self.counterattack.update(5, 1, 40.0, {99: {"team": 1, "x": 80.0}}, fps=30)
        self.buildup.update(1, 0, 5, 20.0)
        self.buildup.update(30, 0, 10, 80.0)
        
        os.makedirs(out_dir, exist_ok=True)
        self.buildup.export(out_dir)
        self.compactness.export(out_dir)
        self.positional.export(out_dir)
        self.counterattack.export(out_dir)
        self.state_engine.export(out_dir)
        self.predictive.export(out_dir)
        
        return True
