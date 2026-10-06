FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_HOME=/app/.cache/huggingface

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# CPU-only PyTorch keeps the image far smaller than the default CUDA wheels
# (the app runs Qwen2.5-VL and CLIP on CPU).
COPY requirements.txt ./
RUN pip install --extra-index-url https://download.pytorch.org/whl/cpu torch torchvision \
    && pip install -r requirements.txt

# The real Streamlit app lives in Drip/ (entry point: "Fashion AI Advisor.py")
COPY Drip/ ./Drip/
COPY Scripts/ ./Scripts/

RUN useradd --create-home app \
    && mkdir -p Images Closet .cache/huggingface \
    && chown -R app:app /app
USER app

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Secrets are NOT baked into the image: pass MONGO_URI at runtime
# (docker run --env-file .env ...).
ENTRYPOINT ["streamlit", "run", "Drip/Fashion AI Advisor.py", \
            "--server.port=8501", "--server.address=0.0.0.0"]
