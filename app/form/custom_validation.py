"""
Документация модуля
"""

from wtforms.validators import ValidationError


class CustomLength:
    """
    Документация класса
    """

    def __init__(self, min_text=-1, max_text=-1, message=None):
        self.min_text = min_text
        self.max_text = max_text
        self.message = message

    def __call__(self, form, field):
        data = field.data or ""
        if self.min_text != -1 and len(data) < self.min_text:
            raise ValidationError(self.message or f"Слишком коротко, минимум {self.min_text} символов")
        if self.max_text != -1 and len(data) > self.max_text:
            raise ValidationError(self.message or f"Слишком длинно, максимум {self.max_text} символов")


class CheckRecord:
    """
    Документация класса
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if field.data is None or str(field.data).strip() == '':
            raise ValidationError(self.message or 'Поле не должно быть пустым или состоять только из пробелов.')
