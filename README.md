# Шаги запуска приложения
1) В корневой папке создать файл .env и прописать значения пустых ключей, которые были отправлены вместе с проектом:

    - cp .env.example .env
    
2) Подтянуть зависимости из docker-compose файла: 

    - sudo docker compose pull

3) Забилдить docker-compose файл:

    - sudo docker compose build

4) Запустить контейнеры:

    - sudo docker compose up -d

5) Выполните скрипт в корневой папке для миграции alembic:

    - ./migrate.sh
