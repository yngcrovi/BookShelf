FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

WORKDIR /app


COPY ./poetry/pyproject.toml ./
COPY ./poetry/poetry.lock ./
COPY ./src ./src

RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry install --no-root --no-dev
RUN poetry update

COPY . .

EXPOSE 8000