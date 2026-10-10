"""Text-to-CadQuery with an execution verifier and one repair round, on the public Text2CAD-Bench preview.

    uv run python t2c.py submit  --style pro --limit 10      # send a generation batch (Message Batches API)
    uv run python t2c.py submit  --style pro --model claude-sonnet-5-5   # another generator; results stay keyed by batch id
    uv run python t2c.py submit  --style pro --fix-encoding  # only the prompts whose GBK symbols were garbled, now decoded
    uv run python t2c.py fetch   <batch_id>                  # save the results under runs/<batch_id>/code/
    uv run python t2c.py spec                                # one batch: each part's overall size, read from both texts
    uv run python t2c.py fetch   <spec_batch_id>             # writes runs/<spec_batch_id>/spec.json
    uv run python t2c.py verify  runs/<batch_id> [runs/<spec_batch_id>/spec.json]   # run every program
    uv run python t2c.py repair  runs/<batch_id>             # repair batch: failed runs and size mismatches
    uv run python t2c.py report  runs/<batch_id> [runs/<repair_id>]                 # before / after one repair

Data: data/release.csv from huggingface.co/datasets/AICAD/Text2CAD-Bench (CC BY 4.0), the 30% preview
(151 prompts, L1-L3; ground-truth STEP files are not public). So this measures whether a program runs
and yields a valid solid, not whether it matches the intended part: the "invalid rate" here is ours,
not the leaderboard's IR (whose definition the README does not give).

The API key is read from %USERPROFILE%/.anthropic/text2cad_api.env (one line, the key) and passed to the
client only; it is never printed or put in the environment, so Claude Code's own login is untouched.
"""
import ast
import codecs
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


def gbk_fix(err):
    """The released CSV mixes UTF-8 with two-byte GBK symbols (degree, plus-minus): decode those bytes as GBK."""
    chunk = err.object[err.start:err.start + 2]
    try:
        return chunk.decode("gbk"), err.start + 2
    except UnicodeDecodeError:
        return "�", err.start + 1


codecs.register_error("gbk_fix", gbk_fix)


def prompts(style: str, limit: int | None, fix_encoding: bool = False):
    # the runs of 2026-10-08 read the file with errors="replace", so the model saw U+FFFD where the CSV holds GBK bytes
    rows = list(csv.DictReader(open(ROOT / "data" / "release.csv", encoding="utf-8-sig",
                                    errors="gbk_fix" if fix_encoding else "replace")))
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
    first, _, rest = body.partition("\n")
    return rest if first.strip().isidentifier() or not first.strip() else body  # drop a language tag line


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


SPEC_SYSTEM = (
    "You read a description of a mechanical part and state the overall size of the finished part: the extents of "
    "its axis-aligned bounding box in millimetres, three numbers. Count every feature that sticks out; holes, "
    "grooves and pockets do not change the box unless they remove a whole outer face. If the description does not "
    "fix all three extents, use null. Reply with one JSON object and nothing else: "
    '{"bbox": [x, y, z] or null, "why": "one short sentence"}'
)


def dims_close(got, exp) -> bool:
    """Extents compared sorted, so the part may lie in any orientation; 2% or 0.5 mm per axis."""
    return all(abs(g - e) <= max(0.5, 0.02 * e) for g, e in zip(sorted(got), sorted(exp)))


def spec_merge(run: Path) -> dict:
    """Pair the size read from the pro text with the one read from the geo text of the same part; only parts
    where both readings exist and agree get an expected size (the two texts were written separately, so an
    agreement is less likely to be one misreading)."""
    got = {}
    for f in (run / "spec").glob("*.txt"):
        cid, style = f.stem.rsplit("__", 1)
        try:
            bbox = json.loads(code_block(f.read_text(encoding="utf-8")).strip()).get("bbox")
        except (json.JSONDecodeError, AttributeError):
            bbox = None
        ok = isinstance(bbox, list) and len(bbox) == 3 and all(isinstance(v, (int, float)) and v > 0 for v in bbox)
        got.setdefault(cid, {})[style] = sorted(bbox) if ok else None
    spec = {}
    for cid, s in sorted(got.items()):
        p, g = s.get("pro"), s.get("geo")
        agree = bool(p and g and dims_close(p, g))
        spec[cid] = {"bbox": [round((a + b) / 2, 3) for a, b in zip(p, g)] if agree else None,
                     "pro": p, "geo": g, "agree": agree}
    (run / "spec.json").write_text(json.dumps(spec, indent=1), encoding="utf-8")
    n = len(spec)
    print(f"spec: {n} parts, both readings {sum(1 for v in spec.values() if v['pro'] and v['geo'])}, "
          f"agree {sum(v['agree'] for v in spec.values())}")
    return spec


def submit(rows, tag: str, messages_for, system: str = SYSTEM, model: str | None = None) -> str:
    model = model or MODEL
    reqs = [{"custom_id": cid, "params": {"model": model, "max_tokens": MAX_TOKENS, "system": system,
                                         "messages": messages_for(cid, text)}} for cid, text in rows]
    b = client().messages.batches.create(requests=reqs)
    d = ROOT / "runs" / b.id
    d.mkdir(parents=True, exist_ok=True)
    (d / "meta.json").write_text(json.dumps({"batch": b.id, "tag": tag, "model": model, "n": len(reqs),
                                             "created": time.strftime("%Y-%m-%dT%H:%M:%S")}, indent=1), encoding="utf-8")
    print(b.id, len(reqs), "requests")
    return b.id


def fetch(batch_id: str) -> None:
    c = client()
    b = c.messages.batches.retrieve(batch_id)
    print(b.processing_status, b.request_counts)
    if b.processing_status != "ended":
        return
    tag = json.loads((ROOT / "runs" / batch_id / "meta.json").read_text(encoding="utf-8"))["tag"]
    is_spec = tag == "spec"
    d = ROOT / "runs" / batch_id / ("spec" if is_spec else "code")
    d.mkdir(parents=True, exist_ok=True)
    usage = {"in": 0, "out": 0, "errors": 0, "truncated": 0}  # truncated: replies cut at MAX_TOKENS
    for r in c.messages.batches.results(batch_id):
        if r.result.type != "succeeded":
            usage["errors"] += 1
            continue
        m = r.result.message
        usage["in"] += m.usage.input_tokens
        usage["out"] += m.usage.output_tokens
        usage["truncated"] += m.stop_reason == "max_tokens"
        text = "".join(x.text for x in m.content if x.type == "text")
        if is_spec:
            (d / f"{r.custom_id}.txt").write_text(text, encoding="utf-8")
        else:
            (d / f"{r.custom_id}.py").write_text(code_block(text), encoding="utf-8")
    (d.parent / "usage.json").write_text(json.dumps(usage), encoding="utf-8")
    print("saved", len(list(d.iterdir())), "files", usage)
    if is_spec:
        spec_merge(d.parent)


def load_spec(path: str | None) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8")) if path else {}


def verify(run: Path, spec: dict | None = None) -> None:
    rows = []
    for f in sorted((run / "code").glob("*.py")):
        res = run_program(f.read_text(encoding="utf-8"))
        res["id"] = f.stem
        exp = (spec or {}).get(f.stem, {}).get("bbox")
        if res["stage"] == "ok" and exp:
            res["dims"] = "match" if dims_close(res["bbox"], exp) else "mismatch"
            res["expected_bbox"] = exp
        rows.append(res)
        print(f.stem, res["stage"], res.get("dims", ""), res.get("error", "")[:80])
    (run / "verify.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")


def recheck(run: Path, spec: dict, timeout_s: int) -> None:
    """Run again, one at a time with a longer limit, only the programs whose first check timed out, and write the new
    result in place (the old one is kept as `first_timeout`). A timeout depends on how busy the machine was; the
    verdict should not (2026-10-08: the same 151 prompts timed out 20 times, then 3 times, under different load)."""
    global TIMEOUT_S
    TIMEOUT_S = timeout_s
    rows = [json.loads(l) for l in (run / "verify.jsonl").read_text(encoding="utf-8").splitlines()]
    for r in rows:
        if r["stage"] != "timeout":
            continue
        res = run_program((run / "code" / f"{r['id']}.py").read_text(encoding="utf-8"))
        exp = (spec or {}).get(r["id"], {}).get("bbox")
        if res["stage"] == "ok" and exp:
            res["dims"] = "match" if dims_close(res["bbox"], exp) else "mismatch"
            res["expected_bbox"] = exp
        res.update(id=r["id"], first_timeout=True, recheck_timeout_s=timeout_s)
        r.clear()
        r.update(res)
        print(r["id"], r["stage"], r.get("dims", ""))
    (run / "verify.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")


def repair(run: Path) -> None:
    meta = json.loads((run / "meta.json").read_text(encoding="utf-8"))
    style = meta["tag"].split(":")[0]
    text = dict(prompts(style, None))
    fails = [json.loads(l) for l in (run / "verify.jsonl").read_text(encoding="utf-8").splitlines()]
    fails = [f for f in fails if f["stage"] != "ok" or f.get("dims") == "mismatch"]

    def feedback(err) -> str:
        if err["stage"] != "ok":
            return f"Running it failed at the {err['stage']} stage: {err.get('error')}."
        return (f"It runs, but the part's bounding box is {err['bbox']} mm, while the description implies "
                f"extents of {err['expected_bbox']} mm (in any order).")

    def messages_for(cid, desc):
        prev = (run / "code" / f"{cid}.py").read_text(encoding="utf-8")
        err = next(f for f in fails if f["id"] == cid)
        return [{"role": "user", "content": desc},
                {"role": "assistant", "content": f"```python\n{prev}\n```"},
                {"role": "user", "content": f"{feedback(err)} Fix the program. Same rules. "
                                            "Reply with one Python code block."}]
    print(len(fails), "to repair")
    submit([(f["id"], text[f["id"]]) for f in fails], f"{style}:repair-of-{run.name}", messages_for,
           model=meta["model"])  # the repair uses the generator of the run it repairs


def rows_of(run: Path) -> dict:
    return {r["id"]: r for r in map(json.loads, (run / "verify.jsonl").read_text(encoding="utf-8").splitlines())}


def summary(name: str, rows: dict) -> None:
    by = {}
    for r in rows.values():
        b = by.setdefault(r["id"].split("_")[0], {"n": 0, "invalid": 0, "checked": 0, "match": 0})
        b["n"] += 1
        b["invalid"] += r["stage"] != "ok"
        b["checked"] += "dims" in r
        b["match"] += r.get("dims") == "match"
    tot = {k: sum(b[k] for b in by.values()) for k in ("n", "invalid", "checked", "match")}
    print(f"{name}: invalid {tot['invalid']}/{tot['n']} | size match {tot['match']}/{tot['checked']} of the parts "
          f"with an agreed expected size |", {k: f"inv {b['invalid']}/{b['n']}, match {b['match']}/{b['checked']}"
                                               for k, b in sorted(by.items())})


def report(base: Path, repaired: Path | None = None) -> None:
    """Before = the generation run; after = the same run with each repaired part's new result in its place."""
    rows = rows_of(base)
    summary(f"{base.name} before repair", rows)
    if repaired:
        after = {**rows, **rows_of(repaired)}
        summary(f"after one repair round ({repaired.name})", after)


def fix_encoding_rows(style: str, limit: int | None) -> list:
    """Only the prompts the GBK decode changes (30 pro, 12 geo): the ones the model saw with U+FFFD in them."""
    fixed = prompts(style, limit, fix_encoding=True)
    return [f for f, raw in zip(fixed, prompts(style, limit)) if f[1] != raw[1]]


def main() -> int:
    global MODEL
    cmd = sys.argv[1]
    if "--model" in sys.argv:
        MODEL = sys.argv[sys.argv.index("--model") + 1]
    if cmd == "submit":
        style = sys.argv[sys.argv.index("--style") + 1] if "--style" in sys.argv else "pro"
        limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else None
        fix = "--fix-encoding" in sys.argv
        submit(fix_encoding_rows(style, limit) if fix else prompts(style, limit),
               f"{style}:generate" + ("-fixenc" if fix else ""), lambda cid, t: [{"role": "user", "content": t}])
    elif cmd == "spec":  # one batch: the overall size read separately from the pro and the geo text of each part
        pro, geo = dict(prompts("pro", None)), dict(prompts("geo", None))
        rows = [(f"{cid}__pro", pro[cid]) for cid in pro] + [(f"{cid}__geo", geo[cid]) for cid in geo]
        submit(rows, "spec", lambda cid, t: [{"role": "user", "content": t}], SPEC_SYSTEM)
    elif cmd == "fetch":
        fetch(sys.argv[2])
    elif cmd == "verify":
        verify(Path(sys.argv[2]), load_spec(sys.argv[3] if len(sys.argv) > 3 else None))
    elif cmd == "recheck":  # recheck runs/<batch> runs/<spec>/spec.json [seconds]
        recheck(Path(sys.argv[2]), load_spec(sys.argv[3]), int(sys.argv[4]) if len(sys.argv) > 4 else 180)
    elif cmd == "repair":
        repair(Path(sys.argv[2]))
    elif cmd == "report":
        report(Path(sys.argv[2]), Path(sys.argv[3]) if len(sys.argv) > 3 else None)
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
        assert dims_close([30, 10, 20], [10.1, 20, 29.5]) and not dims_close([10, 20, 30], [10, 20, 40])
        garbled = {s: {cid for cid, t in prompts(s, None) if "�" in t} for s in ("pro", "geo")}
        fixed = {s: {cid for cid, _ in fix_encoding_rows(s, None)} for s in ("pro", "geo")}
        assert fixed == garbled and (len(fixed["pro"]), len(fixed["geo"])) == (30, 12), {s: len(v) for s, v in fixed.items()}
        assert all("�" not in t for _, t in fix_encoding_rows("pro", None)), "GBK decode left U+FFFD in a pro prompt"
        global TIMEOUT_S
        slow = "import cadquery as cq\nfor i in range(30000000):\n    pass\nresult = cq.Workplane().box(1, 1, 1)"
        TIMEOUT_S = 1
        short = run_program(slow)["stage"]
        TIMEOUT_S = 120
        long_ = run_program(slow)["stage"]
        TIMEOUT_S = 60
        print(f"timeout knob: 1 s -> {short}, 120 s -> {long_}")
        assert (short, long_) == ("timeout", "ok"), (short, long_)
        with tempfile.TemporaryDirectory() as t:
            s = Path(t) / "spec"
            s.mkdir()
            (s / "A_1__pro.txt").write_text('{"bbox": [60, 40, 40], "why": "x"}', encoding="utf-8")
            (s / "A_1__geo.txt").write_text('```json\n{"bbox": [40, 60, 40.2]}\n```', encoding="utf-8")
            (s / "A_2__pro.txt").write_text('{"bbox": [10, 10, 10]}', encoding="utf-8")
            (s / "A_2__geo.txt").write_text('{"bbox": null}', encoding="utf-8")
            (s / "A_3__pro.txt").write_text('{"bbox": [10, 10, 10]}', encoding="utf-8")
            (s / "A_3__geo.txt").write_text('{"bbox": [10, 10, 20]}', encoding="utf-8")
            sp = spec_merge(Path(t))
            assert sp["A_1"]["agree"] and sp["A_1"]["bbox"] == [40.0, 40.1, 60.0], sp["A_1"]
            assert not sp["A_2"]["agree"] and not sp["A_3"]["agree"] and sp["A_3"]["bbox"] is None
        print("selftest ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
