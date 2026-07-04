import os
import yaml
import pandas as pd
from pathlib import Path
from matchmind.core.logger import logger
from matchmind.data.manager import DatasetValidator # type: ignore

class MatchMindTrainer:
    def __init__(self, config):
        self.config = config
        
    def _generate_dataset_yaml(self, dataset_path, yaml_path, classes):
        """Generates dataset.yaml for YOLO training"""
        data = {
            "path": str(Path(dataset_path).resolve()),
            "train": "train/images",
            "val": "valid/images",
            "test": "test/images",
            "names": {i: name for i, name in enumerate(classes)}
        }
        with open(yaml_path, "w") as f:
            yaml.dump(data, f, sort_keys=False)
        logger.info(f"Generated dataset config at: {yaml_path}")
        
    def _update_readme_with_results(self, run_dir):
        """Extracts metrics from results.csv and appends them to README.md"""
        results_file = Path(run_dir) / "results.csv"
        if not results_file.exists():
            logger.warning("results.csv not found. Cannot update README.")
            return
            
        try:
            df = pd.read_csv(results_file)
            # YOLO results.csv headers often have spaces
            df.columns = df.columns.str.strip()
            
            # Get last row (best epoch)
            best_epoch = df.iloc[-1]
            
            p = best_epoch.get("metrics/precision(B)", 0.0)
            r = best_epoch.get("metrics/recall(B)", 0.0)
            mAP50 = best_epoch.get("metrics/mAP50(B)", 0.0)
            mAP50_95 = best_epoch.get("metrics/mAP50-95(B)", 0.0)
            
            readme_path = Path("README.md")
            with open(readme_path, "a") as f:
                f.write("\n## Model Training Results\n")
                f.write(f"- **Precision**: {p:.4f}\n")
                f.write(f"- **Recall**: {r:.4f}\n")
                f.write(f"- **mAP50**: {mAP50:.4f}\n")
                f.write(f"- **mAP50-95**: {mAP50_95:.4f}\n")
                f.write("\n")
                
            logger.success("Updated README.md with training metrics.")
        except Exception as e:
            logger.error(f"Failed to parse results.csv: {e}")
            
    def train(self):
        """
        Executes the fully automated YOLO11 training pipeline.
        Enforces strict dataset validation before allowing training.
        """
        logger.info("Initializing Training Pipeline...")
        
        # 1. Dataset Validation
        validator = DatasetValidator(self.config)
        is_valid = validator.validate_all()
        
        if not is_valid:
            logger.error("❌ Dataset validation failed. Training aborted.")
            logger.error("Please check dataset_validation_report.md for missing files.")
            return False
            
        logger.success("✅ Dataset validation passed. Proceeding to training.")
        
        try:
            from ultralytics import YOLO # type: ignore
        except ImportError:
            logger.error("ultralytics package not found. Please install it to run training.")
            return False
            
        # 2. Get Dataset Config
        # For simplicity, we grab the first YOLO dataset from the config
        datasets = self.config.get("datasets", {})
        target_dataset = None
        target_cfg = None
        for name, cfg in datasets.items():
            if cfg.get("format") == "yolo" and cfg.get("validate"):
                target_dataset = name
                target_cfg = cfg
                break
                
        if not target_dataset:
            logger.error("No valid YOLO dataset found in configuration to train on.")
            return False
            
        dataset_path = Path(target_cfg.get("path"))
        classes = target_cfg.get("classes", ["player", "ball", "referee"])
        
        # 3. Generate dataset.yaml
        yaml_path = dataset_path / "dataset_generated.yaml"
        self._generate_dataset_yaml(dataset_path, yaml_path, classes)
        
        # 4. Configure & Begin YOLO11 Training
        logger.info("Initializing YOLO11 model...")
        model = YOLO("yolo11n.pt") # Load base model
        
        logger.info("Starting training on GPU (TensorBoard, Confusion Matrix, and Checkpoints are automated by Ultralytics)...")
        training_cfg = self.config.get("training", {})
        
        # Base config that cannot be overridden by user
        base_cfg = {
            "data": str(yaml_path),
            "project": "runs/train",
            "name": "matchmind_yolo",
            "exist_ok": True,
            "save": True,
            "plots": True,
            "device": 0
        }
        
        # Merge dicts
        final_cfg = {**training_cfg, **base_cfg}
        
        results = model.train(**final_cfg)
        
        logger.success("Training completed.")
        
        # 5. Export trained weights & Update README
        run_dir = Path("runs/train/matchmind_yolo")
        best_pt = run_dir / "weights/best.pt"
        
        if best_pt.exists():
            out_dir = Path("outputs/weights")
            out_dir.mkdir(parents=True, exist_ok=True)
            import shutil
            shutil.copy(best_pt, out_dir / "custom_yolo11.pt")
            logger.success(f"Exported best weights to {out_dir / 'custom_yolo11.pt'}")
            
        self._update_readme_with_results(run_dir)
        
        return True
