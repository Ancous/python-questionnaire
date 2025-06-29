## <u>Кратко</u>

Создание собственного пакета в Python включает в себя организацию структуры каталогов, создание необходимых файлов,
таких как `__init__.py`, и использование setup.py для установки пакета.

## <u>Развернуто</u>

Создание собственного пакета в Python — это процесс, который позволяет организовать и повторно использовать код.
Пакеты могут содержать модули, классы и функции, которые можно импортировать в другие проекты. Вот шаги для
создания пакета:

1. **Структура каталогов**
    - Для начала создайте основную директорию для Вашего пакета. Внутри этой директории создайте подкаталог с именем
      Вашего пакета и добавьте файл `__init__.py`, который позволяет Python распознавать каталог как пакет.
    ```python
    my_package/
        my_package/
            __init__.py
            module1.py
            module2.py
        setup.py
        README.md
    ```
    - `my_package/` — основная директория Вашего проекта.
    - `my_package/` — подкаталог, содержащий Ваш код.
    - `__init__.py` — файл, который может содержать инициализацию пакета.
    - `module1.py`, `module2.py` — модули, содержащие функции и классы.
    - `setup.py` — файл для установки пакета.
    - `README.md` — файл с описанием Вашего пакета.

2. **Создание файла `__init__.py`**
    - Файл `__init__.py` может быть пустым или содержать код, который будет выполнен при импорте пакета. Вы можете
      также определить, какие функции или классы будут доступны при импорте пакета.
    - Пример `__init__.py`:
    ```Python
    from .module1 import function1
    from .module2 import function2
    ```

3. **Создание модулей**
    - В модулях Вы можете определять функции и классы. Например, module1.py может выглядеть так:
    ```Python
    def function1():
        return "Hello from function1!"
    ```
    - А module2.py:
    ```Python
    def function2():
        return "Hello from function2!"
    ```

4. **Создание файла setup.py**
    - Файл setup.py используется для установки вашего пакета и может содержать метаданные, такие как имя пакета, версия
      и автор. Пример:
    ```Python
    from setuptools import setup, find_packages

    setup(
        name='my_package',
        version='0.1',
        packages=find_packages(),
        description='A simple example package',
        author='Your Name',
        author_email='your.email@example.com',
        url='https://github.com/yourusername/my_package',
    )
    ```

5. **Установка пакета**
    - После того как Вы создали структуру и файлы, Вы можете установить пакет локально, используя команду:
    ```python
    pip install .
    ```
    - Это установит Ваш пакет, и Вы сможете импортировать его в других проектах.

6. **Тестирование пакета**
    - Для тестирования вашего пакета можно создать отдельный файл test.py или использовать фреймворки для тестирования,
      такие как unittest или pytest:
    ```Python
    from my_package import function1, function2

    print(function1())  # Выведет: Hello from function1!
    print(function2())  # Выведет: Hello from function2!
    ```

7. **Публикация пакета**
    - Если Вы хотите сделать Ваш пакет доступным для других, Вы можете опубликовать его на PyPI (Python Package Index).
      Для этого Вам нужно будет зарегистрироваться на PyPI и использовать инструменты, такие как twine, для загрузки
      Вашего пакета.
    ```python
    python setup.py sdist bdist_wheel
    twine upload dist/*

8. **Пример использования**
    ```Bash
    # Создание пакета
    mkdir my_package
    cd my_package
    mkdir my_package
    touch my_package/__init__.py
    touch my_package/module1.py
    touch my_package/module2.py
    touch setup.py
    touch README.md

    # Заполнение файлов
    echo "def function1(): return 'Hello from function1!'" > my_package/module1.py
    echo "def function2(): return 'Hello from function2!'" > my_package/module2.py
    echo "from .module1 import function1\nfrom .module2 import function2" > my_package/__init__.py

    # Создание setup.py
    echo "from setuptools import setup, find_packages\nsetup(name='my_package', version='0.1', packages=find_packages())" > setup.py

    # Установка пакета
    pip install .
    ```

Это основные шаги для создания собственного пакета в Python, включая структуру, файлы и процесс установки.

<div align="right">

[Вернуться к вопросам](../Вопросы.md)

</div>
