# API для социальной сети Yatube
## Описание
Данный API разработан для использования функционала социальной сети Yatube с помощью запросов

##### Стек:
* Python 3.9.10
* Djando 3.2.16
* DRF 3.12.4

##### Основные возможности:
* Просматривать, создавать новые, удалять и изменять публикации.
* Просматривать группы.
* Комментировать, смотреть, удалять и обновлять комментарии.
* Подписаться на других пользователей
* Фильтрация и поиск по полям.

#### Полная документация доступна по адресу `http://localhost:8000/redoc/`
## Как запустить проект
Клонировать репозиторий и перейти в него в командной строке:

```
$ git clone https://github.com/BuhulkTV/api_final_yatube.git
```


```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

## Примеры запросов к api:

Запрос JWT токена с использованием логина и пароля методом POST

```
http://localhost:8000/api/v1/jwt/create/
```

Body запроса

```
{
    "username": "string",
    "password": "string"
}
```

Ответ на запрос

```
{
    "refresh": "string",
    "access": "string"
}
```

Чтобы получить список всех постов используйте метод GET:

```
localhost:8000/api/v1/posts/
```

Ответ на запрос

```
{
"count": 123,
"next": "http://api.example.org/accounts/?offset=400&limit=100",
"previous": "http://api.example.org/accounts/?offset=200&limit=100",
"results": [
    {
        "id": 0,
        "author": "string",
        "text": "string",
        "pub_date": "2021-10-14T20:41:29.648Z",
        "image": "string",
        "group": 0
    }
]
}
```

Все запросы и их методы доступны по в документации к API по ссылке:

```
http://localhost:8000/redoc/
```
