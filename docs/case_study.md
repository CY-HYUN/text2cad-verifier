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
