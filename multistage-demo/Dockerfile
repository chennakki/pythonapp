# syntax=docker/dockerfile:1

# ---------- Stage 1: builder ----------
# Installs runtime dependencies into an isolated virtualenv.
FROM python:3.12-slim AS builder

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt


# ---------- Stage 2: test ----------
# Reuses the builder layer, adds dev deps, runs the tests.
# Run on its own with:  docker build --target test -t demo:test .
FROM builder AS test

COPY requirements-dev.txt .
RUN pip install -r requirements-dev.txt

COPY pytest.ini .
COPY app/ ./app/
COPY tests/ ./tests/
RUN pytest -q


# ---------- Stage 3: runtime ----------
# Final image: slim base + venv + app code only (no pip cache, no tests, no dev deps).
FROM python:3.12-slim AS runtime

ARG APP_VERSION=dev
ENV APP_VERSION=${APP_VERSION} \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN useradd --create-home --uid 10001 appuser
WORKDIR /srv

COPY --from=builder /opt/venv /opt/venv
COPY app/ ./app/

USER appuser
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD python -c "import urllib.request as u; u.urlopen('http://127.0.0.1:8000/health', timeout=2)" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "app.main:app"]
