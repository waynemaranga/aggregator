FROM python:3.10-slim
WORKDIR /app
COPY pyproject.toml requirements.txt ./
RUN python3 -m pip install --no-cache-dir uv \
    && python3 -m venv .venv \
    && .venv/bin/pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["/app/.venv/bin/python", "normalise.py"]