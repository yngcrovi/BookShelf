# Шаги запуска приложения
1) Подтянуть зависимости из docker-compose файла: 

    - sudo docker compose pull

2) Забилдить docker-compose файл:

    - sudo docker compose build

3) Запустить контейнеры:

    - sudo docker compose up -d

4) Выполните скрипт в корневой папке для миграции alembic:

    - ./migrate.sh

5) В корневой папке создать файл .env и прописать значения пустых ключей, которые были отправлены вместе с проектом:

    - cp .env.example .env
