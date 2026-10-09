"""Pack what the Space shows into one file: prompts, generated and repaired programs, their verdicts and the
agreed sizes. Run from the repo root after a new run: `uv run python space/build_data.py`."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import t2c  # noqa: E402

GEN = {"pro": "msgbatch_01YGeeSyynmt9bEaZ4rVMQMi", "geo": "msgbatch_017JfqoG4M6iuL9JMLdEax74"}
REPAIR = {"pro": "msgbatch_01S9gvp5FtKNt7SGdmfywLgm", "geo": "msgbatch_01RPo71YiG8cP8mAhgQF1BfT"}
SPEC = "msgbatch_01JJL4qEqYR94drqWV24gQ5h"


def batch(name: str) -> dict:
    d = ROOT / "results" / name
    rows = [json.loads(l) for l in (d / "verify.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    code = {p.stem: p.read_text(encoding="utf-8") for p in sorted((d / "code").glob("*.py"))}
    return {"batch": name, "verdict": {r["id"]: r for r in rows}, "code": code}


def main() -> int:
    out = {"model": t2c.MODEL, "prompts": {s: dict(t2c.prompts(s, None)) for s in GEN},
           "gen": {s: batch(b) for s, b in GEN.items()}, "repair": {s: batch(b) for s, b in REPAIR.items()},
           "spec": json.loads((ROOT / "results" / SPEC / "spec.json").read_text(encoding="utf-8"))}
    n = {s: len(out["gen"][s]["code"]) for s in GEN}
    assert n == {"pro": 151, "geo": 151}, n  # one program per prompt in both generation runs
    path = Path(__file__).with_name("demo_data.json")
    path.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    print(path, path.stat().st_size, "bytes", n, {s: len(out["repair"][s]["code"]) for s in REPAIR})
    return 0


if __name__ == "__main__":
    sys.exit(main())
