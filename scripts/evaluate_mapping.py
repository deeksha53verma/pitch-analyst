import os
import sys
import cv2
import numpy as np
from pathlib import Path
sys.path.append(os.path.abspath("src")) # type: ignore

from matchmind.core.config import load_config # type: ignore
from matchmind.mapping.homography import PitchMapper # type: ignore
from matchmind.mapping.visualizer import PitchVisualizer # type: ignore
from matchmind.core.logger import logger # type: ignore

def main():
    logger.info("Initializing Pitch Mapping Evaluation...")
    cfg = load_config(config_name="main")
    
    mapper = PitchMapper(cfg)
    viz = PitchVisualizer(cfg)
    
    logger.info("Simulating Homography matrix computation...")
    # Mocking standard broadcast camera angles roughly wrapping half the pitch
    src_pts = np.array([[100, 200], [1800, 200], [1920, 1080], [0, 1080]], dtype=np.float32)
    # Mapping them to the 2D plane (say, the right half of the pitch)
    dst_pts = np.array([[52.5, 0], [105, 0], [105, 68], [52.5, 68]], dtype=np.float32)
    
    mapper.compute_homography(src_pts, dst_pts)
    logger.success("Homography Matrix successfully computed!")
    
    # Simulating player detections in camera view
    logger.info("Transforming player coordinates to BEV...")
    p1_cam = (960, 600)  # Somewhere near the center
    p2_cam = (1500, 800) # Near the goal
    
    p1_bev = mapper.transform_point(*p1_cam)
    p2_bev = mapper.transform_point(*p2_cam)
    
    logger.info(f"Player 1: Camera {p1_cam} -> BEV {p1_bev}")
    logger.info(f"  Zone: {mapper.get_zone(p1_bev)}") # type: ignore
    
    logger.info(f"Player 2: Camera {p2_cam} -> BEV {p2_bev}")
    logger.info(f"  Zone: {mapper.get_zone(p2_bev)}") # type: ignore
    
    # Draw visualization
    logger.info("Rendering beautiful 2D pitch...")
    canvas = viz.draw_pitch()
    
    # Plot entities (P1 is Team 0, P2 is Team 1, Ball near P1)
    logger.info("Plotting entities onto pitch map...")
    players = [
        (p1_bev[0], p1_bev[1], 0), # type: ignore
        (p2_bev[0], p2_bev[1], 1)  # type: ignore
    ]
    ball = (p1_bev[0] + 1.0, p1_bev[1]) # type: ignore
    
    canvas = viz.plot_entities(canvas, players, ball)
    
    out_dir = Path("outputs/evaluation/mapping")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = str(out_dir / "birds_eye_view.jpg")
    
    cv2.imwrite(out_file, canvas)
    logger.success(f"Bird's-Eye View successfully rendered and saved to {out_file}!")

if __name__ == "__main__":
    main()
