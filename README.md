# text2cad-verifier

How often does a frontier LLM write CAD code that runs, and how often does the part come out the right size?
And does one round of feedback from a verifier fix what it gets wrong?

This repo measures both on the public preview of Text2CAD-Bench, with a model writing CadQuery (Python) code
through the Anthropic Message Batches API. One-page summary: [docs/case_study.md](docs/case_study.md).

## What is measured

Two verifiers, run on every generated program:

1. **Execution verifier** (surface check). The program runs in a separate process with a 60 s limit, imports only
   `cadquery` and `math` (an AST allow-list, checked before running), and must leave a variable `result` holding a
   solid that passes OpenCascade's `BRepCheck` with a positive volume.
2. **Size verifier** (does it match the description?). The ground-truth STEP files of the benchmark are not public,
   so the expected size comes from the text itself. The same model reads each part's overall bounding box, in mm,
   separately from the two descriptions the dataset gives for every part (`pro_prompt_en`, a step-by-step modelling
   procedure, and `geo_prompt_en`, a geometric description). A part gets an expected size only when the two
   readings agree within 2% or 0.5 mm per axis. The generated solid's bounding box is then compared with it, with
   the axes sorted, so the part may lie in any orientation.

The repair round sends each failure back once, with the verifier's message: the run error, or "the bounding box is
X mm while the description implies Y mm".

## Data

`data/release.csv`: the 30% preview of [AICAD/Text2CAD-Bench](https://huggingface.co/datasets/AICAD/Text2CAD-Bench)
(CC BY 4.0), 151 prompts in three levels: L1 60, L2 61, L3 30. One id, `L2_40`, is used for two different prompts
(a notch and a groove); both are kept, the second as `L2_40_dup2`.

## Run it

```
uv sync
uv run python t2c.py selftest
uv run python t2c.py submit --style pro            # one batch, 151 programs
uv run python t2c.py spec                          # one batch, 302 size readings
uv run python t2c.py fetch <batch_id>              # repeat per batch once it has ended
uv run python t2c.py verify runs/<gen_batch> runs/<spec_batch>/spec.json
uv run python t2c.py repair runs/<gen_batch>
uv run python t2c.py report runs/<gen_batch> [runs/<repair_batch>]
```

The API key is read from `%USERPROFILE%/.anthropic/text2cad_api.env` and passed to the client only. Generated code
runs on your machine: the allow-list blocks every import except `cadquery` and `math`, and the builtins that reach
files, the OS or dynamic code. Read `safety_problem()` in `t2c.py` before running other people's outputs.

## Results (2026-10-08, model `claude-opus-5-5`, 151 prompts per run)

Expected sizes: 132 of 151 parts got a size from both descriptions, and the two readings agreed on 120 (spec batch
`msgbatch_01JJL4qEqYR94drqWV24gQ5h`). A hand check of six agreed sizes, two per level, found all six right.

| Run | Prompt style | Batch | Programs that fail to run or give no valid solid | Size mismatches (of parts with an agreed size that ran) |
|---|---|---|---|---|
| Generation | pro | `msgbatch_01YGeeSyynmt9bEaZ4rVMQMi` | 4 | 3 of 117 |
| Same prompts again (noise) | pro | `msgbatch_01N7DeL55NxFdKBFA4uaTa3G` | 6 | 2 of 114 |
| Generation | geo | `msgbatch_017JfqoG4M6iuL9JMLdEax74` | 3 | 8 of 117 |
| After one repair round | pro | repair `msgbatch_01S9gvp5FtKNt7SGdmfywLgm` (7 sent) | 1 | 0 of 119 |
| After one repair round | geo | repair `msgbatch_01RPo71YiG8cP8mAhgQF1BfT` (11 sent) | 1 | 0 of 119 |

- **Noise.** The same 151 prompts, generated twice, differ by 2 run failures and 1 size mismatch. One repair round
  took the failures from 7 to 1 (pro) and from 11 to 1 (geo), well outside that.
- **By level.** L1 (60 simple parts) almost never fails; what fails is L2 and L3 (sweeps, lofts, patterns).
- **Timeouts were the machine, not the model.** The first checks ran while another job held the CPU: 66 programs
  timed out at 60 s, and 64 of them ran fine when re-run alone with a 180 s limit (`t2c.py recheck`). The table uses
  the re-run results; a run that still timed out at 180 s counts as a failure.
- **Cost.** 7 batches, about 0.30 M input and 0.45 M output tokens, about $5 at Batch API prices.
- **Files.** `results/<batch id>/` holds each run's generated programs, `verify.jsonl` (one row per program) and
  usage; the spec batch holds `spec.json`. `uv run python t2c.py report results/<generation> results/<repair>`
  reproduces the table without any API call.

What the repair numbers do and do not show: the size feedback told the model the expected box, so a size match
after repair is measured by the same check that guided it. It shows the model can act on the feedback, not that the
repaired part is right in every other feature. A run failure fixed after repair is a stronger signal, because the
feedback only quoted the error.

## Limits

- The size verifier checks one thing: the overall box. A part with the right box and a missing hole passes it.
- The expected size is a model's reading of the text, not a measurement. Agreement between two separately written
  descriptions makes a misreading less likely, not impossible. A hand check of six agreed sizes, two per level,
  found all six right (seed 20261008).
- One repeat run (pro style) measures the noise; geo has no repeat.
- No ground-truth geometry: the benchmark's STEP files are not public, so neither IoU nor Chamfer distance is reported.
- A run that timed out depends on the machine; the 180 s re-run is this repo's rule, not the benchmark's.
