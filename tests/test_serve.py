"""API tests: a valid box with the right size, a refused import, a bad size field. Run: uv run --extra serve --with pytest pytest tests/test_serve.py"""
import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from serve import app  # noqa: E402

client = TestClient(app)


def test_box_runs_and_matches_size():
    r = client.post("/verify", json={"code": "import cadquery as cq\nresult = cq.Workplane('XY').box(40, 20, 10)",
                                     "expected_bbox_mm": [10, 20, 40]})
    assert r.status_code == 200 and r.json()["ok"] and r.json()["size_match"] is True


def test_unsafe_import_is_refused_before_running():
    r = client.post("/verify", json={"code": "import os\nresult = None"})
    assert r.status_code == 200 and r.json()["stage"] == "safety" and not r.json()["ok"]


def test_bad_size_is_a_client_error():
    r = client.post("/verify", json={"code": "result = 1", "expected_bbox_mm": [1, -2, 3]})
    assert r.status_code == 422
