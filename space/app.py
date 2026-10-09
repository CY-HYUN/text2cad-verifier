"""Hugging Face Space: browse the committed Text2CAD-Bench runs and run the two verifiers on CPU.

No API key and no model call: the generated programs are the ones committed under results/, and the
"Try your own" tab runs code the visitor pastes through the same safety check and verifier as t2c.py.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import gradio as gr

HERE = Path(__file__).resolve().parent
ROOT = HERE if (HERE / "t2c.py").exists() else HERE.parent  # Space root, or space/ inside the repo
sys.path.insert(0, str(ROOT))
import t2c  # noqa: E402

# Built by build_data.py. The Space holds only the code; it reads the data file from the GitHub repo at a fixed commit.
DATA_URL = "https://raw.githubusercontent.com/CY-HYUN/text2cad-verifier/{ref}/space/demo_data.json"
DATA_REF = "418947479cb75a84bb971c76cf79449a9ad2ff75"  # commit that holds the demo_data.json this page was tested with


def load_data() -> dict:
    local = HERE / "demo_data.json"
    if local.exists():
        return json.loads(local.read_text(encoding="utf-8"))
    import urllib.request
    with urllib.request.urlopen(DATA_URL.format(ref=DATA_REF), timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


DATA = load_data()
SPEC, PROMPTS = DATA["spec"], DATA["prompts"]
IDS = list(PROMPTS["pro"])

RENDER = r'''
import sys
import cadquery as cq
ns = {"cq": cq, "__name__": "generated"}
exec(compile(open(sys.argv[1], encoding="utf-8").read(), "generated.py", "exec"), ns)
res = ns["result"]
shape = res.val() if isinstance(res, cq.Workplane) and len(res.vals()) == 1 else (
    cq.Compound.makeCompound([v for v in res.vals() if isinstance(v, cq.Shape)]) if isinstance(res, cq.Workplane) else res)
cq.exporters.export(shape, sys.argv[2])
'''


def code_of(run: str, style: str, pid: str) -> str:
    return DATA[run][style]["code"].get(pid, "")


def verdict_of(run: str, style: str, pid: str):
    return DATA[run][style]["verdict"].get(pid)


def expected_of(pid: str):
    s = SPEC.get(pid) or {}
    return s.get("bbox") if s.get("agree") else None


def verdict_text(v: dict | None, expected) -> str:
    if not v:
        return "not run"
    if v.get("stage") != "ok":
        return f"FAILS at {v.get('stage')}: {v.get('error', '')}"
    size = "no agreed size to compare" if not expected else (
        "size matches" if t2c.dims_close(v["bbox"], expected) else f"size mismatch: expected {expected}")
    return f"runs, valid solid, box {v['bbox']} mm, {v['solids']} solid(s), {size}"


def render(src: str) -> str | None:
    """STL of the program's result for the viewer, or None when it does not build."""
    if t2c.safety_problem(src):
        return None
    d = Path(tempfile.mkdtemp())
    (d / "gen.py").write_text(src, encoding="utf-8")
    (d / "render.py").write_text(RENDER, encoding="utf-8")
    try:
        subprocess.run([sys.executable, "-I", str(d / "render.py"), str(d / "gen.py"), str(d / "part.stl")],
                       capture_output=True, timeout=t2c.TIMEOUT_S, cwd=d)
    except subprocess.TimeoutExpired:
        return None
    return str(d / "part.stl") if (d / "part.stl").exists() else None


def show_part(pid: str, style: str):
    expected = expected_of(pid)
    gen, rep = verdict_of("gen", style, pid), verdict_of("repair", style, pid)
    repaired = code_of("repair", style, pid)
    record = (f"**First attempt:** {verdict_text(gen, expected)}\n\n"
              f"**After one repair round:** {verdict_text(rep, expected) if repaired else 'not needed (first attempt passed both checks)'}\n\n"
              f"**Expected size (two readings of the text agree):** {expected if expected else 'none'}")
    return PROMPTS[style].get(pid, ""), code_of("gen", style, pid), repaired, record


def run_code(src: str, expected_text: str = ""):
    expected = None
    if expected_text.strip():
        try:
            expected = [float(x) for x in expected_text.replace("x", ",").split(",")]
            assert len(expected) == 3
        except (ValueError, AssertionError):
            return "Expected size must be three numbers, e.g. 20, 50, 57.7", None
    if not src.strip():
        return "No code to run.", None
    v = t2c.run_program(src)
    return verdict_text(v, expected), render(src) if v.get("stage") == "ok" else None


def run_stored(pid: str, style: str, which: str):
    src = code_of("repair" if which == "repaired" else "gen", style, pid)
    return run_code(src, ",".join(map(str, expected_of(pid) or [])))


INTRO = """# text2cad-verifier
How often does a frontier LLM (`claude-opus-5-5`) write CadQuery code that runs, and does the part come out the right size?
151 prompts from the public preview of [Text2CAD-Bench](https://huggingface.co/datasets/AICAD/Text2CAD-Bench) (CC BY 4.0).
Two checks: **execution** (runs in a separate process, imports only `cadquery` and `math`, leaves a valid solid with positive
volume) and **size** (the overall bounding box against the size the text implies, when two separate readings of the text agree).
Code and results: [GitHub](https://github.com/CY-HYUN/text2cad-verifier). This page calls no model: it shows the committed runs and re-runs the checks on CPU."""

with gr.Blocks(title="text2cad-verifier") as demo:
    gr.Markdown(INTRO)
    with gr.Tab("Benchmark parts"):
        with gr.Row():
            part = gr.Dropdown(IDS, value=IDS[0], label="Part (L1 simple, L2 medium, L3 hard)")
            style = gr.Radio(["pro", "geo"], value="pro", label="Prompt style (step-by-step or geometric description)")
        prompt = gr.Textbox(label="Prompt given to the model", lines=6, interactive=False)
        record = gr.Markdown()
        with gr.Row():
            first = gr.Code(label="First attempt", language="python", interactive=False)
            fixed = gr.Code(label="After the verifier's feedback (only for parts that failed)", language="python", interactive=False)
        with gr.Row():
            which = gr.Radio(["first attempt", "repaired"], value="first attempt", label="Run which program now")
            go = gr.Button("Run the checks now (CPU, up to 60 s)", variant="primary")
        live = gr.Textbox(label="Result of this run", interactive=False)
        view = gr.Model3D(label="Part", height=420)
        for ev in (part.change, style.change, demo.load):
            ev(show_part, [part, style], [prompt, first, fixed, record])
        go.click(run_stored, [part, style, which], [live, view])
    with gr.Tab("Try your own CadQuery"):
        gr.Markdown("Paste a program that assigns the part to `result`. Only `cadquery` and `math` may be imported; "
                    "file, OS and dynamic-code builtins are refused before anything runs.")
        src = gr.Code(value="import cadquery as cq\nresult = cq.Workplane('XY').box(40, 20, 10).faces('>Z').hole(6)",
                      language="python", label="CadQuery program")
        exp = gr.Textbox(label="Expected size in mm, optional (three numbers, any order)", placeholder="40, 20, 10")
        go2 = gr.Button("Run the checks", variant="primary")
        out2 = gr.Textbox(label="Result", interactive=False)
        view2 = gr.Model3D(label="Part", height=420)
        go2.click(run_code, [src, exp], [out2, view2])

if __name__ == "__main__":
    demo.launch()

