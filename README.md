![foodgram-project-react Workflow Status](https://github.com/chuvichkin/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg?branch=master&event=push)
# Продуктовый помощник Foodgram

Проект доступен по адресу http://158.160.4.80

## Описание проекта Foodgram
«Продуктовый помощник»: приложение, на котором пользователи публикуют рецепты, подписываться на публикации других авторов и добавлять рецепты в избранное. Сервис «Список покупок» позволит пользователю создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

## Запуск с использованием CI/CD

Установить docker, docker-compose на сервере ВМ Yandex.Cloud:
```bash
ssh username@ip
sudo apt update && sudo apt upgrade -y && sudo apt install curl -y
sudo curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh && sudo rm get-docker.sh
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
- Создайте файл .env в директории infra:

```bash
touch .env
```
- Заполните .env, согласно настройкам БД:

```python
DB_ENGINE='django.db.backends.postgresql'
DB_NAME=
POSTGRES_USER=
POSTGRES_PASSWORD=
DB_HOST=db
DB_PORT='5432'
```
- Перенесите файлы docker-compose.yml, .env и default.conf на сервер:

```bash
scp docker-compose.yml username@server_ip:/home/<username>/
scp default.conf <username>@<server_ip>:/home/<username>/
scp .env <username>@<server_ip>:/home/<username>/
```


## Запуск проекта через Docker
- На сервере выполнить команду, чтобы собрать контейнер:
```bash
sudo docker-compose up -d
```

Для доступа к контейнеру выполните следующие команды:

```bash
sudo docker-compose exec backend python manage.py makemigrations
```
```bash
sudo docker-compose exec backend python manage.py migrate
```
```bash
sudo docker-compose exec backend python manage.py createsuperuser
```
```bash
sudo docker-compose exec backend python manage.py collectstatic --no-input
```

Дополнительно можно наполнить DB ингредиентами:

```bash
sudo docker-compose exec backend python manage.py ingredients.json
```

## Запуск проекта в dev-режиме

- Установить и активировать виртуальное окружение:

```bash
source /venv/bin/activated
```

- Установить зависимости из файла requirements.txt

```bash
python -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

- Выполнить миграции:

```bash
python manage.py migrate
```

- В папке с файлом manage.py выполнить команду:
```bash
python manage.py runserver
```

## Автор
- :snake: [Чувычкин Сергей](https://github.com/Chuvichkin)
