from pathlib import Path
from typing import Dict, Any
import numpy as np
import cv2
from omegaconf import DictConfig
from matchmind.core.logger import logger
from ultralytics import YOLO

class YOLODetector:
    def __init__(self, config: DictConfig):
        self.config = config.model
        self.model = None
        self.load(self.config.get("weights_path", "yolo11n.pt"))

    def load(self, weights_path: str):
        """Load YOLO11 model weights."""
        logger.info(f"Loading YOLO11 model from {weights_path}")
        self.model = YOLO(weights_path)
        logger.info(f"Model loaded successfully.")

    def predict_image(self, image: np.ndarray) -> Dict[str, np.ndarray]:
        """Runs inference on a single image array (BGR)."""
        if self.model is None:
            raise ValueError("Model not loaded.")
            
        inf_cfg = self.config.inference
        results = self.model.predict(
            source=image,
            conf=inf_cfg.conf_threshold,
            iou=inf_cfg.iou_threshold,
            imgsz=inf_cfg.img_size,
            max_det=inf_cfg.max_det,
            half=inf_cfg.half,
            device=inf_cfg.device,
            verbose=False
        )
        
        result = results[0]
        boxes = result.boxes.xyxy.cpu().numpy()
        scores = result.boxes.conf.cpu().numpy()
        class_ids = result.boxes.cls.cpu().numpy()
        
        return {
            "boxes": boxes,
            "scores": scores,
            "class_ids": class_ids
        }

    def train(self, data_yaml: str):
        """Trains the YOLO11 model."""
        if self.model is None:
            raise ValueError("Model not initialized for training.")
            
        train_cfg = self.config.training
        logger.info(f"Starting YOLO11 training on {data_yaml}")
        
        self.model.train(
            data=data_yaml,
            epochs=train_cfg.epochs,
            batch=train_cfg.batch_size,
            imgsz=train_cfg.img_size,
            lr0=train_cfg.lr0,
            optimizer=train_cfg.optimizer,
            patience=train_cfg.patience,
            device=self.config.inference.device
        )
        logger.success("Training completed.")

    def evaluate(self, data_yaml: str):
        """Evaluates the YOLO11 model."""
        logger.info(f"Evaluating YOLO11 model on {data_yaml}")
        metrics = self.model.val(data=data_yaml)
        logger.info(f"mAP50-95: {metrics.box.map}")
        return metrics
