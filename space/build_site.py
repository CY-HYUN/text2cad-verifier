"""Static demo for GitHub Pages: docs/demo/ gets index.html (copied from space/site.html), data.json (prompts,
programs, verdicts, sizes from demo_data.json) and one STL per program that builds. Nothing runs in the browser
except the viewer. Run from the repo root: `uv run python space/build_site.py` (after space/build_data.py).

Each committed program is rendered in a worker process that imports cadquery once; programs that fail the safety
check, raise, or take longer than the limit get no STL and the page says so.
"""
import json
import multiprocessing as mp
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = ROOT / "docs" / "demo"
LIMIT_S = 120
sys.path.insert(0, str(ROOT))


def render(job):
    key, src, path = job
    import cadquery as cq
    ns = {"cq": cq, "__name__": "generated"}
    try:
        exec(compile(src, "generated.py", "exec"), ns)
        res = ns["result"]
        shape = res.val() if isinstance(res, cq.Workplane) and len(res.vals()) == 1 else (
            cq.Compound.makeCompound([v for v in res.vals() if isinstance(v, cq.Shape)]) if isinstance(res, cq.Workplane) else res)
        cq.exporters.export(shape, path, tolerance=0.2, angularTolerance=0.3)
        return key, None
    except Exception as e:  # reported per program on the page, never silent
        return key, f"{type(e).__name__}: {e}"[:200]


def main() -> int:
    import t2c
    data = json.loads((HERE / "demo_data.json").read_text(encoding="utf-8"))
    if "--page-only" in sys.argv:  # new data.json and index.html, keep the rendered STL files
        old = json.loads((OUT / "data.json").read_text(encoding="utf-8"))
        data["stl"], data["stl_errors"] = old["stl"], old["stl_errors"]
        (OUT / "data.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        shutil.copy(HERE / "site.html", OUT / "index.html")
        print("data.json and index.html rewritten; STL kept:", len(data["stl"]))
        return 0
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "stl").mkdir(parents=True)
    jobs, skipped = [], {}
    for run in ("gen", "repair"):
        for style, b in data[run].items():
            for pid, src in b["code"].items():
                key = f"{run}_{style}_{pid}"
                problem = t2c.safety_problem(src)
                if problem:
                    skipped[key] = problem
                    continue
                jobs.append((key, src, str(OUT / "stl" / f"{key}.stl")))
    errors = dict(skipped)
    with mp.Pool(4, maxtasksperchild=20) as pool:
        pending = [(j[0], pool.apply_async(render, (j,))) for j in jobs]
        for key, p in pending:
            try:
                _, err = p.get(timeout=LIMIT_S)
            except mp.TimeoutError:
                err = f"no STL in {LIMIT_S} s"
            if err:
                errors[key] = err
    stl = sorted(p.stem for p in (OUT / "stl").glob("*.stl"))
    data["stl"] = stl
    data["stl_errors"] = errors
    (OUT / "data.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    shutil.copy(HERE / "site.html", OUT / "index.html")
    size = sum(p.stat().st_size for p in (OUT / "stl").glob("*.stl"))
    print(f"programs {len(jobs) + len(skipped)}, STL {len(stl)} ({size / 1e6:.1f} MB), no STL {len(errors)}")
    for k, v in list(errors.items())[:10]:
        print("  ", k, v)
    return 0


if __name__ == "__main__":
    sys.exit(main())
