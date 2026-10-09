"""Pack what the Space shows into one file: prompts, generated and repaired programs, their verdicts and the
agreed sizes. Run from the repo root after a new run: `uv run python space/build_data.py`."""
import codecs
import csv
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import t2c  # noqa: E402

GEN = {"pro": "msgbatch_01YGeeSyynmt9bEaZ4rVMQMi", "geo": "msgbatch_017JfqoG4M6iuL9JMLdEax74"}
REPAIR = {"pro": "msgbatch_01S9gvp5FtKNt7SGdmfywLgm", "geo": "msgbatch_01RPo71YiG8cP8mAhgQF1BfT"}
SPEC = "msgbatch_01JJL4qEqYR94drqWV24gQ5h"


def gbk_fix(err):
    """The public CSV mixes UTF-8 with GBK-encoded symbols (degree, plus-minus). Decode those two bytes as GBK."""
    chunk = err.object[err.start:err.start + 2]
    try:
        return chunk.decode("gbk"), err.start + 2
    except UnicodeDecodeError:
        return "�", err.start + 1


codecs.register_error("gbk_fix", gbk_fix)


def prompts_readable(style: str) -> dict:
    """Same rows and ids as t2c.prompts, but with the GBK symbols decoded (t2c read them as U+FFFD, and so did the model)."""
    text = (ROOT / "data" / "release.csv").read_bytes().decode("utf-8-sig", errors="gbk_fix")
    rows = list(csv.DictReader(io.StringIO(text)))
    col = {"pro": "pro_prompt_en", "geo": "geo_prompt_en"}[style]
    out, seen = {}, {}
    for r in rows:
        if not r.get(col):
            continue
        n = seen[r["id"]] = seen.get(r["id"], 0) + 1
        out[r["id"] if n == 1 else f"{r['id']}_dup{n}"] = r[col]
    return out


def batch(name: str) -> dict:
    d = ROOT / "results" / name
    rows = [json.loads(l) for l in (d / "verify.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    code = {p.stem: p.read_text(encoding="utf-8") for p in sorted((d / "code").glob("*.py"))}
    return {"batch": name, "verdict": {r["id"]: r for r in rows}, "code": code}


def main() -> int:
    sent = {s: dict(t2c.prompts(s, None)) for s in GEN}
    shown = {s: prompts_readable(s) for s in GEN}
    assert {s: list(v) for s, v in sent.items()} == {s: list(v) for s, v in shown.items()}  # same ids, same order
    garbled = {s: sorted(p for p, t in sent[s].items() if "�" in t) for s in GEN}
    out = {"model": t2c.MODEL, "prompts": shown, "garbled_as_sent": garbled,
           "gen": {s: batch(b) for s, b in GEN.items()}, "repair": {s: batch(b) for s, b in REPAIR.items()},
           "spec": json.loads((ROOT / "results" / SPEC / "spec.json").read_text(encoding="utf-8"))}
    n = {s: len(out["gen"][s]["code"]) for s in GEN}
    assert n == {"pro": 151, "geo": 151}, n  # one program per prompt in both generation runs
    path = Path(__file__).with_name("demo_data.json")
    path.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    print(path, path.stat().st_size, "bytes", n, {s: len(out["repair"][s]["code"]) for s in REPAIR},
          "| prompts sent with U+FFFD:", {s: len(v) for s, v in garbled.items()},
          "| still U+FFFD after GBK decode:", {s: sum("�" in t for t in shown[s].values()) for s in GEN})
    return 0


if __name__ == "__main__":
    sys.exit(main())
