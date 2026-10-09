# Serves the verifier API (serve.py). The program under test runs in a child process with the allow-list from t2c.py.
FROM python:3.12-slim
# OpenCascade (cadquery-ocp) needs these shared libraries on a slim image
RUN apt-get update && apt-get install -y --no-install-recommends libgl1 libglib2.0-0 libxrender1 libxext6 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
RUN pip install --no-cache-dir "cadquery==2.8.0" "fastapi>=0.115" "uvicorn>=0.30"
COPY t2c.py serve.py ./
RUN useradd --create-home app && chown -R app /app
USER app
EXPOSE 8000
CMD ["uvicorn", "serve:app", "--host", "0.0.0.0", "--port", "8000"]
