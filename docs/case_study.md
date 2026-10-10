# Case study: a verifier that says what "correct" means for text-to-CAD

**Question.** When a frontier model writes CAD code from a text description, how often does the part run, and how
often is it the right size? And does one round of verifier feedback fix what it gets wrong?

**Setup.** The public preview of Text2CAD-Bench: 151 descriptions of mechanical parts in three levels (60 simple,
61 medium, 30 complex), each written two ways, a modelling procedure and a geometric description. The model writes
CadQuery code through the Message Batches API. Every program runs in its own process under an import allow-list.

**Two verifiers.**

1. *Does it run?* The program must finish and leave one valid solid with positive volume (OpenCascade's own check).
2. *Is it the right size?* The benchmark's ground-truth STEP files are not public, so the expected size comes from
   the text. The model reads each part's overall bounding box separately from the two descriptions, and a part gets
   an expected size only when the two readings agree. 120 of 151 parts did. Six of them, checked by hand, were right.

**What I measured.**

| | Run failures | Size mismatches (parts with an agreed size that ran) |
|---|---|---|
| First generation (procedure text) | 4 of 151 | 3 of 117 |
| Same prompts again | 6 of 151 | 2 of 114 |
| After one repair round | 1 of 151 | 0 of 119 |

The repeat run is the noise floor: two failures and one size mismatch either way. One repair round, with the
verifier's message as feedback, fixed 6 of 7 failures. On the geometric descriptions it fixed 10 of 11.

**What went wrong along the way, and what it taught.**

- *A timeout is not a verdict.* The first checks ran while another job held the CPU. 66 programs timed out at 60
  seconds, and 64 of them ran fine alone at 180 seconds. A verifier's time budget has to be part of its definition,
  or a busy machine reads as a weak model.
- *A feedback signal is not an independent test.* The size feedback told the model the expected box, so "size match
  after repair" is measured by the check that guided the fix. It shows the model can act on the feedback. It does
  not show the rest of the part is right; that needs the ground truth, which is not public.
- *The data had a duplicate id* (two different prompts under one id). Both are kept and counted.

**Where this goes next.** A feature-level verifier (holes, threads, counts) built the same way, from what the text
states, and a held-out check of the repaired parts against the benchmark's ground truth when it is released.

Code, prompts, every generated program and every verdict: this repository. The table reproduces offline with
`uv run python t2c.py report results/<generation> results/<repair>`.

## Appendix (2026-10-10): other generators, a geo repeat, and the encoding fix

Same protocol as above: same prompts, system prompt and 4,000-token reply limit, the same expected sizes (the
Opus 5.5 readings of `results/msgbatch_01JJL4qEqYR94drqWV24gQ5h/spec.json`, for every generator), a 60 s check with
every timeout re-run alone at 180 s, and one repair round by the model that wrote the program. New runs:
`t2c.py submit --style pro --model claude-sonnet-5-5` (or `claude-haiku-4-5-20251001`).

**Generators.** Run failures are of 151; size mismatches are of the parts with an agreed size that ran.

| Generator | Style | Generation batch | Run failures | Size mismatches | Repair batch (sent) | Fixed in one round | After repair: failures, mismatches | Cost |
|---|---|---|---|---|---|---|---|---|
| Opus 5.5 | pro | `msgbatch_01YGeeSyynmt9bEaZ4rVMQMi` | 4 | 3 of 117 | `msgbatch_01S9gvp5FtKNt7SGdmfywLgm` (7) | 6 of 7 | 1, 0 of 119 | $1.30 + $0.14 |
| Opus 5.5 | geo | `msgbatch_017JfqoG4M6iuL9JMLdEax74` | 3 | 8 of 117 | `msgbatch_01RPo71YiG8cP8mAhgQF1BfT` (11) | 10 of 11 | 1, 0 of 119 | $1.19 + $0.20 |
| Sonnet 5.5 | pro | `msgbatch_01Mp9La7iX8DNKXthWS6AjU5` | 8 | 5 of 114 | `msgbatch_01GpLzdQTpQsS17EXzXbo5pe` (13) | 10 of 13 | 3, 0 of 118 | $0.65 + $0.11 |
| Sonnet 5.5 | geo | `msgbatch_01AfxJ4NW7zhB7SFLuKojMJh` | 3 | 5 of 117 | `msgbatch_015SufxUoA5J4hDaQ8q4B4SA` (8) | 5 of 8 | 3, 0 of 117 | $0.59 + $0.10 |
| Haiku 4.5 | pro | `msgbatch_01PqWws5ZBmBE9xYwRuhdJjj` | 83 | 12 of 60 | `msgbatch_017Fm2YMEBSFPA8HfpNE1Y3r` (95) | 23 of 95 | 56, 16 of 81 | $0.28 + $0.18 |
| Haiku 4.5 | geo | `msgbatch_01LesPnttd6AAgxi4bJsWLze` | 63 | 19 of 75 | `msgbatch_01KzsZmUELjCfrsGaRcpiXaV` (82) | 22 of 82 | 40, 20 of 92 | $0.29 + $0.19 |

**Noise.** The same prompts and model, run again:

| Generator | Style | Batch | Run failures | Size mismatches |
|---|---|---|---|---|
| Opus 5.5 | pro (repeat, 2026-10-08) | `msgbatch_01N7DeL55NxFdKBFA4uaTa3G` | 6 | 2 of 114 |
| Opus 5.5 | geo (repeat, 2026-10-10) | `msgbatch_01RbRG84vD7XhAvoL9AGWAoe` | 5 | 5 of 115 |

**Encoding fix.** The released CSV stores ° and ± as GBK bytes inside UTF-8, and the runs read them as U+FFFD, so 30
pro and 12 geo prompts reached the model with broken characters. `t2c.py submit --fix-encoding` sends only those
prompts, decoded. Opus 5.5, counted on those prompts only:

| Style | Prompts | As sent on 2026-10-08 (broken) | Same, run again (broken) | Decoded | Cost |
|---|---|---|---|---|---|
| pro | 30 | 0 failures, 0 of 29 mismatches | 2, 0 of 27 (`msgbatch_01N7DeL55NxFdKBFA4uaTa3G`) | 0, 0 of 29 (`msgbatch_01RxVk6SZqAC4hRN9gRaA3JU`) | $0.25 |
| geo | 12 | 0 failures, 2 of 7 mismatches | 2, 0 of 5 (`msgbatch_01RbRG84vD7XhAvoL9AGWAoe`) | 2, 0 of 5 (`msgbatch_01FE8N7iXFoTFucDxh9a5Apa`) | $0.18 |

**What it shows.**

- *Sonnet 5.5 is close to Opus 5.5.* On geo it matches the two Opus runs (3 failures vs 3 and 5). On pro it failed 8
  times against Opus's 4 and 6, with 6 of the 8 in L3. One run per model cannot separate that from noise. Its size
  mismatches (5 and 5) sit inside the Opus range (2 to 8).
- *Haiku 4.5 often writes CadQuery that does not exist.* 83 of 151 pro and 63 of 151 geo programs fail to run.
  52 and 38 of those failures are `AttributeError`, `TypeError` or `NameError`, for example `Workplane.workplaneFromFace`
  or `Sketch.moveTo`; the Opus and Sonnet generation runs have none. One repair round with the error message fixes about a
  quarter (23 of 95, 22 of 82), against 6 of 7 and 10 of 11 for Opus. Its size mismatches are counted only on the
  parts that ran, mostly easier ones, so they do not compare directly with the other rows.
- *Geo has the same noise as pro.* Opus on geo, twice: 3 and 5 failures, 8 and 5 size mismatches. The gap between pro
  and geo mismatches on 2026-10-08 (3 vs 8) is within that spread.
- *The encoding fix changes nothing measurable.* On both styles the decoded run lands where a repeat with the broken
  text lands. One of the two decoded geo failures (`L3_24`) is a reply cut at the 4,000-token limit.
- *The reply limit shows up in repairs too.* 3 of the 8 Sonnet geo repair replies hit 4,000 tokens (`truncated` in
  that batch's `usage.json`); 2 of its 3 remaining failures have no `result` variable.

**Reproduce.** Each generator row: `uv run python t2c.py report results/<generation> results/<repair>`; noise rows:
`uv run python t2c.py report results/<batch>`. An encoding row, for one style and batch:
`uv run python -c "import sys, t2c, pathlib; s, b = sys.argv[1:]; ids = [i for i, _ in t2c.fix_encoding_rows(s, None)]; r = t2c.rows_of(pathlib.Path('results', b)); print(len(ids), sum(r[i]['stage'] != 'ok' for i in ids), sum(r[i].get('dims') == 'mismatch' for i in ids), sum('dims' in r[i] for i in ids))" geo msgbatch_01FE8N7iXFoTFucDxh9a5Apa`.

**Cost** is computed, not read from the billing console: the token counts in each `results/<batch>/usage.json` times
the Message Batches prices per million input / output tokens (half of list price: Opus 5.5 $2 / $10, Sonnet 5.5
$1 / $5, Haiku 4.5 $0.50 / $2.50; Anthropic price table as of 2026-09-25). The 11 batches of 2026-10-10 come to
$4.02; the 7 Opus batches of 2026-10-08, the same way, to $5.14.
