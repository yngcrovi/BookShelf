FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    && apt-get clean

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

COPY poetry/pyproject.toml poetry/poetry.lock ./

RUN pip install --upgrade pip

RUN pip install poetry && poetry install --no-root
RUN poetry update
RUN pip install grpcio grpcio-tools
RUN pip install pika
RUN pip install aio_pika
RUN pip install python-dotenv
RUN pip install sqlalchemy
RUN pip install pydantic_settings
RUN pip install psycopg-binary
RUN pip install psycopg

COPY . .

EXPOSE 50051

CMD ["python3", "start_grpc_server.py"]
