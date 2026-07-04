import os
import sys
sys.path.append(os.path.abspath("src")) # type: ignore

from matchmind.identity.engine import IdentityEngine # type: ignore
from matchmind.core.logger import logger # type: ignore

def main():
    logger.info("Initializing Identity Engine Evaluation...")
    engine = IdentityEngine()
    
    # Simulate data streaming in from Tracker, Classifier, and OCR
    logger.info("Simulating Frame 1 (Initialization)...")
    engine.update(track_id=1, team_id=-1, jersey_number=None)
    engine.update(track_id=2, team_id=-1, jersey_number=None)
    
    # Check identity strings
    logger.info(f"Track 1 Identity: {engine.get_identity(1)}")
    logger.info(f"Track 2 Identity: {engine.get_identity(2)}")
    
    logger.info("Simulating Frame 10 (Teams locked in)...")
    engine.update(track_id=1, team_id=0, jersey_number=None)
    engine.update(track_id=2, team_id=1, jersey_number=None)
    
    logger.info(f"Track 1 Identity: {engine.get_identity(1)}")
    logger.info(f"Track 2 Identity: {engine.get_identity(2)}")
    
    logger.info("Simulating Frame 30 (OCR successfully reads numbers)...")
    engine.update(track_id=1, team_id=0, jersey_number="10")
    engine.update(track_id=2, team_id=1, jersey_number="7")
    
    # Let's add a third player who we never get a number for
    engine.update(track_id=3, team_id=1, jersey_number=None)
    
    logger.success(f"Final Track 1 Identity: {engine.get_identity(1)}")
    logger.success(f"Final Track 2 Identity: {engine.get_identity(2)}")
    logger.success(f"Final Track 3 Identity: {engine.get_identity(3)}")
    
    # Export the final datasets
    out_dir = "outputs/evaluation/identity"
    logger.info(f"Exporting final databases to {out_dir}...")
    engine.export_identities(out_dir)
    engine.export_statistics(out_dir)
    
    logger.success("Identity Engine Evaluation Complete!")

if __name__ == "__main__":
    main()
