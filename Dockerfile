# syntax=docker/dockerfile:1.7
# TriggerMap review application. EXTRAS="serve" (rules/CRF-free) or "serve neural" for
# transformer releases; uv resolves CPU-only PyTorch on Linux from the lockfile.

FROM ghcr.io/astral-sh/uv:0.12.22 AS uv

FROM python:3.12.15-slim-bookworm AS build
ARG EXTRAS="serve"
ENV UV_LINK_MODE=copy UV_COMPILE_BYTECODE=1 UV_PYTHON_DOWNLOADS=never
COPY --from=uv /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock README.md LICENSE ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-install-project $(printf -- '--extra %s ' $EXTRAS)
COPY src ./src
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-editable $(printf -- '--extra %s ' $EXTRAS)

FROM python:3.12.15-slim-bookworm AS runtime
RUN apt-get update \
    && apt-get install -y --no-install-recommends git ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --uid 10001 triggermap \
    && mkdir -p /data /release /work && chown triggermap /data /work
WORKDIR /app
COPY --from=build /app/.venv /app/.venv
COPY configs ./configs
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    HF_HUB_OFFLINE=1 \
    TRANSFORMERS_OFFLINE=1 \
    TRIGGERMAP_DATABASE=/data/triggermap.db
USER triggermap
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD ["python", "-c", "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/readyz', timeout=4).status == 200 else 1)"]
CMD ["triggermap", "app", "run", "--host", "0.0.0.0", "--port", "8000"]
