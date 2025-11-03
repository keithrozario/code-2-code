# Use an official Python runtime as a parent image
FROM ghcr.io/astral-sh/uv:python3.13-alpine

COPY pyproject.toml uv.lock* ./
RUN uv sync --locked

# Set the working directory in the container
WORKDIR /app
COPY ./app ./app

# Expose the port the app runs on
CMD ["sh", "-c", "uv run uvicorn app.main:app --host 0.0.0.0 --port $PORT"]
