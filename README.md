# Yacut

Сервис укорачивания ссылок

### Описание:

YaCut ассоциирует длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или предоставляет сервис.
При переходе по короткой ссылке происходит переадресация на исходный адрес.

Доступ к сервису предоставляется как с помощью графического интерфейса веб страницы, так и через API.

### Запуск проекта

Клонировать репозиторий и перейти в него в командной строке:

```
git clone 
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

### Используемые технологии

- Python
- SQLAlchemy
- Flask

### Автор
Владимир Максимов