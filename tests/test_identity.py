import pytest
import os
import json
from matchmind.identity.engine import IdentityEngine # type: ignore

def test_identity_update():
    engine = IdentityEngine()
    
    # 1. New Player
    engine.update(track_id=1, team_id=0, jersey_number=None)
    assert engine.get_identity(1) == "Team_0_Unknown"
    
    # 2. Add Jersey Number (Simulate OCR success)
    engine.update(track_id=1, team_id=0, jersey_number="10")
    assert engine.get_identity(1) == "Team_0_10"
    
    # 3. Simulate OCR failed read (None). Should NOT overwrite the established number.
    engine.update(track_id=1, team_id=0, jersey_number=None)
    assert engine.get_identity(1) == "Team_0_10"
    
def test_identity_unknowns():
    engine = IdentityEngine()
    engine.update(track_id=2, team_id=-1, jersey_number=None)
    assert engine.get_identity(2) == "Team_Unknown_Unknown"
    
def test_identity_export(tmp_path):
    engine = IdentityEngine()
    engine.update(track_id=1, team_id=0, jersey_number="10")
    engine.update(track_id=2, team_id=1, jersey_number="7")
    
    out_dir = str(tmp_path / "exports")
    engine.export_identities(out_dir)
    engine.export_statistics(out_dir)
    
    assert os.path.exists(os.path.join(out_dir, "identities.csv"))
    assert os.path.exists(os.path.join(out_dir, "identities.json"))
    assert os.path.exists(os.path.join(out_dir, "statistics.json"))
    
    with open(os.path.join(out_dir, "statistics.json"), "r") as f:
        stats = json.load(f)
        assert stats["total_players_tracked"] == 2
        assert stats["identified_jerseys"] == 2
        assert stats["unidentified_jerseys"] == 0
