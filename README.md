# text2cad-verifier

How often does a frontier LLM write CAD code that runs, and how often does the part come out the right size?
And does one round of feedback from a verifier fix what it gets wrong?

This repo measures both on the public preview of Text2CAD-Bench, with a model writing CadQuery (Python) code
through the Anthropic Message Batches API.

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

## Results

Filled in from the run below; every number has its batch id.

## Limits

- The size verifier checks one thing: the overall box. A part with the right box and a missing hole passes it.
- The expected size is a model's reading of the text, not a measurement. Agreement between two separately written
  descriptions makes a misreading less likely, not impossible. A hand check of six agreed sizes, two per level,
  found all six right (seed 20261008).
- One generation per prompt. Run-to-run variation is not yet measured beyond the repeat pairs noted in Results.
