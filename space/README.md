---
title: text2cad-verifier
emoji: 📐
colorFrom: blue
colorTo: gray
sdk: gradio
sdk_version: 6.30.0
python_version: "3.12"
app_file: app.py
pinned: false
short_description: Does LLM-written CadQuery run and come out the right size?
---

Demo of [text2cad-verifier](https://github.com/CY-HYUN/text2cad-verifier): 151 prompts from the public preview of
[Text2CAD-Bench](https://huggingface.co/datasets/AICAD/Text2CAD-Bench) (CC BY 4.0), CadQuery programs written by
`claude-opus-5-5`, and two verifiers (execution, overall size). The page calls no model. It shows the committed runs
(first attempt and one repair round) and re-runs the checks on CPU, or runs CadQuery you paste.

Files: `app.py` (this page), `t2c.py` (the verifier, same file as the repo), `demo_data.json` (built by
`space/build_data.py` in the repo from `results/`).
