"""
Модуль содержит пользовательские валидаторы для форм WTForms.
"""

from wtforms.validators import ValidationError


class CustomLength:
    """
    Класс-валидатор для проверки минимальной и максимальной длины строки в поле формы.

    Arguments:
    min_text (int): минимальная длина текста
    max_text (int): максимальная длина текста
    message (str | None): сообщение об ошибке
    """

    min_text: int
    max_text: int
    message: str | None

    def __init__(
        self, min_text: int = -1, max_text: int = -1, message: str | None = None
    ) -> None:
        """
        Инициализация валидатора длины.

        Parameters:
        min_text (int): минимальная длина текста
        max_text (int): максимальная длина текста
        message (str | None): сообщение об ошибке
        """
        self.min_text = min_text
        self.max_text = max_text
        self.message = message

    def __call__(self, form, field) -> None:
        """
        Проверяет длину значения поля.

        Parameters:
        form: форма, к которой относится поле
        field: поле формы
        """
        data: str = field.data or ""
        if self.min_text != -1 and len(data) < self.min_text:
            raise ValidationError(
                self.message or f"Слишком коротко, минимум {self.min_text} символов"
            )
        if self.max_text != -1 and len(data) > self.max_text:
            raise ValidationError(
                self.message or f"Слишком длинно, максимум {self.max_text} символов"
            )


class CheckRecord:
    """
    Класс-валидатор для проверки, что поле не пустое и не состоит только из пробелов.

    Arguments:
    message (str | None): сообщение об ошибке
    """

    message: str | None

    def __init__(self, message: str | None = None) -> None:
        """
        Инициализация валидатора пустого поля.

        Parameters:
        message (str | None): сообщение об ошибке
        """
        self.message = message

    def __call__(self, form, field) -> None:
        """
        Проверяет, что поле не пустое и не состоит только из пробелов.

        Parameters:
        form: форма, к которой относится поле
        field: поле формы
        """
        if field.data is None or str(field.data).strip() == "":
            raise ValidationError(
                self.message
                or "Поле не должно быть пустым или состоять только из пробелов."
            )
