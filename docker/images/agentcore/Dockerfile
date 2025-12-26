FROM --platform=linux/arm64 python:3.12-slim-bookworm

WORKDIR /app

RUN pip install hatch

COPY pyproject.toml src/ ./
RUN hatch env create

EXPOSE 8080

CMD ["hatch", "run", "agentcore"]