"""
Модуль запускает Flask-приложение через WSGI.
"""

from app import create_app

app = create_app()

def main() -> None:
    """
    Точка входа для запуска Flask-приложения.
    """
    app.run(host="127.0.0.1", port=5000, debug=True)

if __name__ == '__main__':
    main()
