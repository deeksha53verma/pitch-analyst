import pytest
import numpy as np
from omegaconf import OmegaConf
from unittest.mock import patch, MagicMock

from matchmind.detection.yolo import YOLODetector # type: ignore
from matchmind.detection.visualizer import DetectionVisualizer # type: ignore

@pytest.fixture
def mock_cfg():
    return OmegaConf.create({
        "model": {
            "type": "yolo",
            "weights_path": "dummy.pt",
            "classes": {0: "player", 1: "goalkeeper", 2: "referee", 3: "ball"},
            "inference": {
                "img_size": 640,
                "conf_threshold": 0.25,
                "iou_threshold": 0.45,
                "max_det": 300,
                "half": False,
                "device": "cpu"
            },
            "training": {
                "epochs": 1,
                "batch_size": 2,
                "img_size": 640,
                "optimizer": "auto",
                "lr0": 0.01,
                "patience": 5
            }
        }
    })

@patch('matchmind.detection.yolo.YOLO')
def test_yolo_initialization(mock_yolo_class, mock_cfg):
    detector = YOLODetector(mock_cfg)
    mock_yolo_class.assert_called_once_with("dummy.pt")
    assert detector.model is not None

@patch('matchmind.detection.yolo.YOLO')
def test_yolo_predict(mock_yolo_class, mock_cfg):
    # Setup mock results
    mock_model_instance = MagicMock()
    mock_result = MagicMock()
    
    # Mocking ultralytics results box structure
    mock_result.boxes.xyxy.cpu().numpy.return_value = np.array([[10, 10, 50, 50]])
    mock_result.boxes.conf.cpu().numpy.return_value = np.array([0.9])
    mock_result.boxes.cls.cpu().numpy.return_value = np.array([0])
    
    mock_model_instance.predict.return_value = [mock_result]
    mock_yolo_class.return_value = mock_model_instance
    
    detector = YOLODetector(mock_cfg)
    
    dummy_image = np.zeros((100, 100, 3), dtype=np.uint8)
    preds = detector.predict_image(dummy_image)
    
    assert "boxes" in preds
    assert "scores" in preds
    assert "class_ids" in preds
    assert preds["boxes"].shape == (1, 4)
    assert preds["scores"][0] == 0.9

def test_visualizer():
    classes = {0: "player"}
    vis = DetectionVisualizer(classes)
    
    dummy_img = np.zeros((100, 100, 3), dtype=np.uint8)
    boxes = np.array([[10, 10, 50, 50]])
    scores = np.array([0.95])
    class_ids = np.array([0])
    
    out_img = vis.draw(dummy_img, boxes, scores, class_ids)
    
    assert out_img.shape == dummy_img.shape
    # Ensure it's not the exact same array reference (it should be copied)
    assert id(out_img) != id(dummy_img)
