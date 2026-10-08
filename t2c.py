"""Text-to-CadQuery with an execution verifier and one repair round, on the public Text2CAD-Bench preview.

    uv run python t2c.py submit  --style pro --limit 10      # send a generation batch (Message Batches API)
    uv run python t2c.py fetch   <batch_id>                  # save the results under runs/<batch_id>/code/
    uv run python t2c.py verify  runs/<batch_id>             # run every program, write verify.jsonl
    uv run python t2c.py repair  runs/<batch_id>             # send a repair batch for the failures
    uv run python t2c.py report  runs/<batch_id> [runs/<repair_id>]

Data: data/release.csv from huggingface.co/datasets/AICAD/Text2CAD-Bench (CC BY 4.0), the 30% preview
(151 prompts, L1-L3; ground-truth STEP files are not public). So this measures whether a program runs
and yields a valid solid, not whether it matches the intended part: the "invalid rate" here is ours,
not the leaderboard's IR (whose definition the README does not give).

The API key is read from %USERPROFILE%/.anthropic/text2cad_api.env (one line, the key) and passed to the
client only; it is never printed or put in the environment, so Claude Code's own login is untouched.
"""
import ast
import csv
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MODEL = "claude-opus-5-5"  # pinned; a model change is a new run, not a silent swap
MAX_TOKENS = 4000
TIMEOUT_S = 60

SYSTEM = (
    "You write CadQuery (Python) programs that build the described part. Rules: import only cadquery "
    "(as cq) and math; build the whole part and assign the final cq.Workplane or cq.Shape to a variable "
    "named result; no file I/O, no printing, no other imports. Units are millimetres unless the description "
    "says otherwise. Reply with one Python code block and nothing else."
)

ALLOWED_IMPORTS = {"cadquery", "math"}
BANNED_NAMES = {"open", "exec", "eval", "compile", "__import__", "input", "globals", "locals", "vars",
                "getattr", "setattr", "delattr", "breakpoint", "exit", "quit"}


def client():
    import anthropic
    key = (Path(os.environ["USERPROFILE"]) / ".anthropic" / "text2cad_api.env").read_text(encoding="utf-8").strip()
    return anthropic.Anthropic(api_key=key)


def prompts(style: str, limit: int | None):
    rows = list(csv.DictReader(open(ROOT / "data" / "release.csv", encoding="utf-8-sig", errors="replace")))
    col = {"pro": "pro_prompt_en", "geo": "geo_prompt_en"}[style]
    out, seen = [], {}
    for r in rows:
        if not r.get(col):
            continue
        # the public release reuses one id for two different prompts (L2_40 notch / groove): keep both
        n = seen[r["id"]] = seen.get(r["id"], 0) + 1
        out.append((r["id"] if n == 1 else f"{r['id']}_dup{n}", r[col]))
    return out[:limit] if limit else out


def code_block(text: str) -> str:
    if "```" not in text:
        return text.strip()
    body = text.split("```", 2)[1]
    return body.split("\n", 1)[1] if body.startswith(("python", "py")) else body


def safety_problem(src: str) -> str | None:
    """Why this program must not run here, or None. Generated code runs on CY's laptop, so only
    cadquery and math may be imported and no builtin that reaches files, the OS or dynamic code."""
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        return f"syntax: {e.msg} (line {e.lineno})"
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            bad = [a.name for a in node.names if a.name.split(".")[0] not in ALLOWED_IMPORTS]
            if bad:
                return f"import not allowed: {bad}"
        elif isinstance(node, ast.ImportFrom):
            if (node.module or "").split(".")[0] not in ALLOWED_IMPORTS:
                return f"import not allowed: {node.module}"
        elif isinstance(node, ast.Name) and node.id in BANNED_NAMES:
            return f"name not allowed: {node.id}"
        elif isinstance(node, ast.Attribute) and node.attr.startswith("__"):
            return f"dunder attribute not allowed: {node.attr}"
    return None


CHECKER = r'''
import json, sys
import cadquery as cq
ns = {"cq": cq, "__name__": "generated"}
src = open(sys.argv[1], encoding="utf-8").read()
out = {}
try:
    exec(compile(src, "generated.py", "exec"), ns)
except Exception as e:
    print(json.dumps({"stage": "run", "error": f"{type(e).__name__}: {e}"[:400]})); sys.exit(0)
res = ns.get("result")
if res is None:
    print(json.dumps({"stage": "result", "error": "no variable named result"})); sys.exit(0)
try:
    shape = res.val() if isinstance(res, cq.Workplane) and len(res.vals()) == 1 else (
        cq.Compound.makeCompound([v for v in res.vals() if isinstance(v, cq.Shape)]) if isinstance(res, cq.Workplane) else res)
    solids = shape.Solids()
    bb = shape.BoundingBox()
    out = {"stage": "ok", "solids": len(solids), "valid": bool(shape.isValid()),
           "volume": round(sum(s.Volume() for s in solids), 3),
           "bbox": [round(bb.xlen, 3), round(bb.ylen, 3), round(bb.zlen, 3)], "faces": len(shape.Faces())}
    if not solids:
        out.update(stage="geometry", error="no solid in result")
    elif not out["valid"]:
        out.update(stage="geometry", error="shape is not valid (BRepCheck)")
    elif out["volume"] <= 0:
        out.update(stage="geometry", error="non-positive volume")
except Exception as e:
    out = {"stage": "geometry", "error": f"{type(e).__name__}: {e}"[:400]}
print(json.dumps(out))
'''


def run_program(src: str) -> dict:
    problem = safety_problem(src)
    if problem:
        return {"stage": "safety", "error": problem}
    with tempfile.TemporaryDirectory() as d:
        prog, checker = Path(d) / "gen.py", Path(d) / "check.py"
        prog.write_text(src, encoding="utf-8")
        checker.write_text(CHECKER, encoding="utf-8")
        try:
            p = subprocess.run([sys.executable, "-I", str(checker), str(prog)], capture_output=True, text=True,
                               timeout=TIMEOUT_S, cwd=d)
        except subprocess.TimeoutExpired:
            return {"stage": "timeout", "error": f"no result in {TIMEOUT_S} s"}
        lines = [l for l in p.stdout.splitlines() if l.startswith("{")]
        if not lines:
            return {"stage": "crash", "error": (p.stderr.strip().splitlines() or ["no output"])[-1][:400]}
        return json.loads(lines[-1])


def submit(rows, tag: str, messages_for) -> str:
    reqs = [{"custom_id": cid, "params": {"model": MODEL, "max_tokens": MAX_TOKENS, "system": SYSTEM,
                                         "messages": messages_for(cid, text)}} for cid, text in rows]
    b = client().messages.batches.create(requests=reqs)
    d = ROOT / "runs" / b.id
    d.mkdir(parents=True, exist_ok=True)
    (d / "meta.json").write_text(json.dumps({"batch": b.id, "tag": tag, "model": MODEL, "n": len(reqs),
                                             "created": time.strftime("%Y-%m-%dT%H:%M:%S")}, indent=1), encoding="utf-8")
    print(b.id, len(reqs), "requests")
    return b.id


def fetch(batch_id: str) -> None:
    c = client()
    b = c.messages.batches.retrieve(batch_id)
    print(b.processing_status, b.request_counts)
    if b.processing_status != "ended":
        return
    d = ROOT / "runs" / batch_id / "code"
    d.mkdir(parents=True, exist_ok=True)
    usage = {"in": 0, "out": 0, "errors": 0}
    for r in c.messages.batches.results(batch_id):
        if r.result.type != "succeeded":
            usage["errors"] += 1
            continue
        m = r.result.message
        usage["in"] += m.usage.input_tokens
        usage["out"] += m.usage.output_tokens
        (d / f"{r.custom_id}.py").write_text(code_block("".join(x.text for x in m.content if x.type == "text")),
                                             encoding="utf-8")
    (d.parent / "usage.json").write_text(json.dumps(usage), encoding="utf-8")
    print("saved", len(list(d.glob("*.py"))), "programs", usage)


def verify(run: Path) -> None:
    rows = []
    for f in sorted((run / "code").glob("*.py")):
        res = run_program(f.read_text(encoding="utf-8"))
        res["id"] = f.stem
        rows.append(res)
        print(f.stem, res["stage"], res.get("error", "")[:80])
    (run / "verify.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")


def repair(run: Path) -> None:
    meta = json.loads((run / "meta.json").read_text(encoding="utf-8"))
    style = meta["tag"].split(":")[0]
    text = dict(prompts(style, None))
    fails = [json.loads(l) for l in (run / "verify.jsonl").read_text(encoding="utf-8").splitlines()]
    fails = [f for f in fails if f["stage"] != "ok"]

    def messages_for(cid, desc):
        prev = (run / "code" / f"{cid}.py").read_text(encoding="utf-8")
        err = next(f for f in fails if f["id"] == cid)
        return [{"role": "user", "content": desc},
                {"role": "assistant", "content": f"```python\n{prev}\n```"},
                {"role": "user", "content": f"Running it failed at the {err['stage']} stage: {err.get('error')}. "
                                            "Fix the program. Same rules. Reply with one Python code block."}]
    submit([(f["id"], text[f["id"]]) for f in fails], f"{style}:repair-of-{run.name}", messages_for)


def report(runs) -> None:
    for run in runs:
        rows = [json.loads(l) for l in (run / "verify.jsonl").read_text(encoding="utf-8").splitlines()]
        by = {}
        for r in rows:
            lvl = r["id"].split("_")[0]
            by.setdefault(lvl, [0, 0])
            by[lvl][1] += 1
            by[lvl][0] += r["stage"] != "ok"
        stages = {}
        for r in rows:
            stages[r["stage"]] = stages.get(r["stage"], 0) + 1
        print(run.name, f"invalid {sum(v[0] for v in by.values())}/{len(rows)}",
              {k: f"{v[0]}/{v[1]}" for k, v in sorted(by.items())}, stages)


def main() -> int:
    cmd = sys.argv[1]
    if cmd == "submit":
        style = sys.argv[sys.argv.index("--style") + 1] if "--style" in sys.argv else "pro"
        limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else None
        submit(prompts(style, limit), f"{style}:generate", lambda cid, t: [{"role": "user", "content": t}])
    elif cmd == "fetch":
        fetch(sys.argv[2])
    elif cmd == "verify":
        verify(Path(sys.argv[2]))
    elif cmd == "repair":
        repair(Path(sys.argv[2]))
    elif cmd == "report":
        report([Path(a) for a in sys.argv[2:]])
    elif cmd == "selftest":
        assert safety_problem("import os\nresult = 1") == "import not allowed: ['os']"
        assert safety_problem("result = open('x')").startswith("name not allowed")
        assert safety_problem("import cadquery as cq\nresult = cq.Workplane().box(1, 2, 3)") is None
        ok = run_program("import cadquery as cq\nresult = cq.Workplane().box(10, 20, 30)")
        assert ok["stage"] == "ok" and ok["bbox"] == [10.0, 20.0, 30.0] and abs(ok["volume"] - 6000) < 1e-6, ok
        bad = run_program("import cadquery as cq\nresult = cq.Workplane().box(10, 20, 30).fillet(50)")
        assert bad["stage"] != "ok", bad
        none = run_program("import cadquery as cq\nx = 1")
        assert none["stage"] == "result", none
        ids = [i for i, _ in prompts("pro", None)]
        assert len(ids) == len(set(ids)) == 151, (len(ids), len(set(ids)))
        print("selftest ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
