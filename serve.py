"""HTTP API for the two verifiers: POST a CadQuery program, get the execution verdict and, if an expected size is
given, the size verdict. Same checks as t2c.py (allow-list, separate process, time limit); no model is called.

    uv run --extra serve uvicorn serve:app --port 8000      # then open http://127.0.0.1:8000/docs
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

import t2c

app = FastAPI(title="text2cad-verifier", version="0.1.0",
              description="Checks LLM-written CadQuery programs: does it build a valid solid, and is it the expected size?")


class VerifyRequest(BaseModel):
    code: str = Field(..., min_length=1, max_length=50_000, description="CadQuery program that assigns the part to `result`")
    expected_bbox_mm: list[float] | None = Field(None, min_length=3, max_length=3,
                                                 description="Expected overall size in mm, any axis order")


class VerifyResponse(BaseModel):
    stage: str = Field(..., description="ok, or where it failed: safety, run, result, geometry, timeout, crash")
    ok: bool
    error: str | None = None
    bbox_mm: list[float] | None = None
    volume_mm3: float | None = None
    solids: int | None = None
    size_match: bool | None = Field(None, description="null when no expected size was sent or the program failed")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "timeout_s": t2c.TIMEOUT_S}


@app.post("/verify", response_model=VerifyResponse)
def verify(req: VerifyRequest) -> VerifyResponse:
    if req.expected_bbox_mm is not None and any(x <= 0 for x in req.expected_bbox_mm):
        raise HTTPException(status_code=422, detail="expected_bbox_mm must be three positive numbers")
    v = t2c.run_program(req.code)
    ok = v.get("stage") == "ok"
    size = t2c.dims_close(v["bbox"], req.expected_bbox_mm) if ok and req.expected_bbox_mm else None
    return VerifyResponse(stage=v.get("stage", "crash"), ok=ok, error=v.get("error"), bbox_mm=v.get("bbox"),
                          volume_mm3=v.get("volume"), solids=v.get("solids"), size_match=size)
