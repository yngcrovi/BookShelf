# Шаги запуска приложения
1) Подтянуть зависимости из docker-compose файла: 

    - sudo docker compose pull

2) Забилдить docker-compose файл:

    - sudo docker compose build

3) Запустить контейнеры:

    - sudo docker compose up -d

4) Если по какой-то причине какие-то зависимости не установились, перейти в папку poetry и установить зависимости вручную:

    - poetry install
    - poetry update

5) Создайте таблицы с помощью alembic в корневой папке:

    - alembic upgrade head

6) Перейти в файл start_grpc_server.py, который находится в ./src и запустить его отдельно для запуска grpc-сервера:

    python3 start_grpc_server.py

7) В корневой папке создать файл .env и прописать значения пустых ключей, которые были присланы вместе с проектом:

    - cp .env.example .env

8) Перейти в папку src и запустить сервер:

    - uvicorn main:app --reload