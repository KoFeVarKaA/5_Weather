FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
ENV UV_PROJECT_ENVIRONMENT=/app/.venv \
    UV_NO_MANAGED_PYTHON=1 \
    UV_NO_CACHE=true \
    UV_LINK_MODE=copy

RUN apk update && apk add --no-cache gcc musl-dev postgresql-dev

RUN python -m pip install --upgrade pip

RUN adduser -D user
RUN mkdir -p /opt /run && chmod 777 /opt /run

WORKDIR /user

RUN mkdir -p /user/static && chown -R user:user /user && chmod -R 755 /user

COPY --chown=user:user pyproject.toml .
COPY --chown=user:user uv.lock .
ENV PATH=/app/.venv/bin:$PATH
RUN uv sync --all-extras --frozen --no-install-project

COPY --chown=user:user ./siteweather .

USER user