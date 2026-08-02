FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

ENV UV_PROJECT_ENVIRONMENT=/app/.venv \
    UV_NO_MANAGED_PYTHON=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"


RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

RUN adduser --disabled-password --gecos "" user

RUN mkdir -p /opt /run /user/staticfiles && \
    chmod 777 /opt /run && \
    chown -R user:user /user && \
    chmod -R 755 /user

WORKDIR /user

COPY --chown=user:user pyproject.toml .
COPY --chown=user:user uv.lock .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --all-extras --frozen --no-install-project

COPY --chown=user:user ./siteweather .

USER user
