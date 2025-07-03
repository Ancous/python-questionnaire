## <u>Кратко</u>

Подключение к базе данных в Flask обычно реализуется через расширения, такие как `Flask-SQLAlchemy`, которые упрощают
работу с различными СУБД.

## <u>Развернуто</u>

Flask предоставляет минимальный функционал, и для работы с базами данных часто используют сторонние расширения,
обеспечивающие удобные абстракции и интеграцию с ORM.

1. **Выбор библиотеки для работы с базой данных**
    - `Flask-SQLAlchemy` — популярное расширение с поддержкой ORM SQLAlchemy.
    - Другие варианты: `Flask-PyMongo` для MongoDB, `Flask-MySQL` и др.

2. **Основные шаги подключения с Flask-SQLAlchemy**
    - Установить пакет:
    ```bash
    pip install flask-sqlalchemy
    ```  
    - Конфигурировать URL базы данных в настройках Flask:
    ```python
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    ```  
    - Создать объект `SQLAlchemy`, связанный с приложением:
    ```python
    from flask_sqlalchemy import SQLAlchemy
    db = SQLAlchemy(app)
    ```  
    - Определять модели данных как классы, наследующие `db.Model`.

3. **Преимущества и недостатки**
    - **Преимущества:**
        - Простота и удобство интеграции с базами.
        - Управление миграциями, связями и запросами через ORM.
    - **Недостатки:**
        - Некоторая сложность настройки и обучения.
        - Возможные ограничения при использовании сложных или нестандартных SQL-функций.

4. **Контекст использования**
    - Веб-приложения с сохранением и обработкой данных.
    - Прототипирование и масштабируемые проекты.

5. **Пример подключения и модели:**
    ```python
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    db = SQLAlchemy(app)

    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)

    @app.route('/')
    def index():
        users = User.query.all()
        return ', '.join(user.username for user in users)

    if __name__ == '__main__':
        app.run(debug=True)
    ```

Таким образом, подключение к базам данных в Flask обычно осуществляется через расширения типа `Flask-SQLAlchemy`,
предоставляющие удобный API и интеграцию с ORM.

<div align="right">

[Вернуться к вопросам](../Вопросы.md)

</div>
