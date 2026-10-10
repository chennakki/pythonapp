# multistage-demo

Small Flask app serving a static page, built to practice multi-stage Dockerfiles.

## Structure

```
multistage-demo/
├── app/
│   ├── __init__.py
│   ├── main.py            # Flask app: /, /health, /api/info
│   └── static/
│       ├── index.html
│       └── style.css
├── tests/
│   └── test_app.py
├── Dockerfile             # builder -> test -> runtime
├── .dockerignore
├── pytest.ini
├── requirements.txt       # runtime deps
└── requirements-dev.txt   # test deps
```

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q
python -m app.main        # http://localhost:8000
```

## Docker

```bash
# full build (runtime stage is the last stage, so it is the default target)
docker build -t multistage-demo:1.0 --build-arg APP_VERSION=1.0 .
docker run --rm -p 8000:8000 multistage-demo:1.0

# build only up to a given stage
docker build --target builder -t multistage-demo:builder .
docker build --target test    -t multistage-demo:test .

# compare image sizes
docker images | grep multistage-demo
```

## Things to try

- Compare the `builder`, `test` and `runtime` image sizes.
- Add a compiled dependency (e.g. `psycopg2`) to the builder stage and see that build tools never reach runtime.
- Break a test and watch `--target test` fail.
- Enable BuildKit cache mounts: `RUN --mount=type=cache,target=/root/.cache/pip pip install ...`
- Swap the runtime base for `python:3.12-alpine` or a distroless image and compare.
