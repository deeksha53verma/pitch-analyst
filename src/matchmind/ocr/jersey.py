import cv2
import numpy as np
import easyocr # type: ignore
from typing import Dict, Tuple, Optional
from collections import deque
from omegaconf import DictConfig
from matchmind.core.logger import logger

class JerseyOCR:
    def __init__(self, config: DictConfig):
        self.config = config.ocr.params
        
        langs = self.config.get("languages", ["en"])
        use_gpu = self.config.get("use_gpu", True)
        self.conf_thresh = self.config.get("confidence_threshold", 0.3)
        self.temporal_window = self.config.get("temporal_window", 30)
        self.crop_ratio = self.config.get("torso_crop_ratio", [0.15, 0.60])
        
        logger.info(f"Loading EasyOCR (langs={langs}, gpu={use_gpu})...")
        # We only care about numbers
        self.reader = easyocr.Reader(langs, gpu=use_gpu, verbose=False)
        
        # History: track_id -> deque of predicted string numbers
        self.history: Dict[int, deque] = {}
        
    def _extract_torso(self, crop: np.ndarray) -> np.ndarray:
        """Crops out the head and legs, leaving only the torso/back."""
        if crop.size == 0:
            return crop
            
        h, w = crop.shape[:2]
        top_y = int(h * self.crop_ratio[0])
        bottom_y = int(h * self.crop_ratio[1])
        
        if top_y >= bottom_y or bottom_y > h:
            return crop # Fallback if ratios are invalid
            
        return crop[top_y:bottom_y, :]
        
    def _enhance_image(self, torso: np.ndarray) -> np.ndarray:
        """Applies grayscale and CLAHE to make digits highly visible."""
        if torso.size == 0:
            return torso
            
        # Convert to grayscale
        gray = cv2.cvtColor(torso, cv2.COLOR_BGR2GRAY)
        
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        
        # Slightly blur to remove jersey fabric noise
        enhanced = cv2.bilateralFilter(enhanced, 9, 75, 75)
        
        return enhanced
        
    def _run_easyocr(self, img: np.ndarray) -> Tuple[Optional[str], float]:
        """Extracts text using EasyOCR and returns the most likely number."""
        if img.size == 0:
            return None, 0.0
            
        # allowlist='0123456789' forces EasyOCR to only look for digits
        results = self.reader.readtext(img, allowlist='0123456789')
        
        best_num = None
        best_conf = 0.0
        
        for (bbox, text, conf) in results:
            if conf > self.conf_thresh and conf > best_conf:
                # Basic validation (jerseys are usually 1 or 2 digits)
                if text.isdigit() and 1 <= len(text) <= 2:
                    best_num = text
                    best_conf = float(conf)
                    
        return best_num, best_conf
        
    def predict_number(self, track_id: int, crop: np.ndarray) -> Tuple[Optional[str], float]:
        """
        Extracts torso, enhances, runs OCR, and applies temporal voting.
        Returns the stable jersey number (string) and temporal confidence.
        """
        # 1. Image Processing
        torso = self._extract_torso(crop)
        enhanced = self._enhance_image(torso)
        
        # 2. Raw OCR
        raw_num, raw_conf = self._run_easyocr(enhanced)
        
        # 3. Temporal Voting
        if track_id not in self.history:
            self.history[track_id] = deque(maxlen=self.temporal_window)
            
        if raw_num is not None:
            self.history[track_id].append(raw_num)
            
        # If we have no history, return None
        if not self.history[track_id]:
            return None, 0.0
            
        # Majority Vote
        counts = {}
        for num in self.history[track_id]:
            counts[num] = counts.get(num, 0) + 1
            
        best_num = max(counts, key=counts.get) # type: ignore
        vote_conf = counts[best_num] / len(self.history[track_id])
        
        return best_num, vote_conf
