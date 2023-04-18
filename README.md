# Система оценки мнений
***
### Структура проекта
***
<div>
├── <b><i>conf</i></b><br>
│   ├── asgi.py<br>
│   ├── __init__.py<br>
│   ├── settings.py<br>
│   ├── urls.py<br>
│   └── wsgi.py<br>
├── <b><i>main</i></b><br>
│   ├── admin.py<br>
│   ├── apps.py<br>
│   ├── __init__.py<br>
│   ├── migrations<br>
│   ├── models.py<br>
│   ├── tests.py<br>
│   ├── urls.py<br>
│   └── views.py<br>
├── manage.py<br>
├── README.md<br>
├── requirements.txt<br>
├── <b><i>static</i></b><br>
│   ├── css<br>
│   ├── img<br>
│   └── js<br>
├── <b><i>templates</i></b><br>
│   └── main<br>
└── <b><i>venv</i></b><br>
<br>
</div>

`conf/` - все главные настройки 

`main/` - главное приложение проекта

`static/` - статические файлы проекта

`templates/` - шаблоны страниц проекта

`venv/` - виртуальное окружение проекта

---

### Как запустить сайт проекта? (*dev mode*)
***
1. Зайти на сервер.
2. Перейти в директорию 'soo/'.
3. Активировать виртуальное окружение:

    ```bash
    source venv/bin/activate
    ```

4. Запустить сайт:

    ```bash
    python manage.py runserver 0.0.0.0:5000
    ```


***
### Как спарсить посты? (*dev mode*)
***
1. Зайти на сервер.
2. Перейти в директорию 'soo/'.
3. Активировать виртуальное окружение:

    ```bash
    source venv/bin/activate
    ```
4. Открыть песочницу Django:

    ```bash
    python manage.py shell
    ```

5. Импортировать парсер:

    ```python3
    from main.views import Parcer as p
    ```

6. Создать экземпляр класса парсера:

    ```python3
    _ = p()
    ```

7. Вызвать у экземпляра класса функцию get_posts():

    ```python3
    _.get_posts()
    ```
