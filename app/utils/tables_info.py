"""
Модуль для работы с информацией о таблицах базы данных.
Содержит функции для форматирования столбцов таблицы и получения информации о таблицах через инспектор SQLAlchemy.
"""

from typing import Any, List, Dict, Optional, Sequence


def format_columns(columns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Форматирует столбцы таблицы, удаляя лишние поля и приводя тип к строке.

    Parameters:
    columns (List[Dict[str, Any]]): список столбцов таблицы

    Return:
    result (List[Dict[str, Any]]): отформатированный список столбцов
    """
    result: List[Dict[str, Any]] = []
    for column in columns:
        column.pop("default", None)
        column.pop("comment", None)
        column["type"] = str(column["type"])
        result.append(column)
    return result


def inspector_tables(
    inspector: Any, tables_names: Sequence[str], title: Optional[str] = None
) -> Optional[Any]:
    """
    Получает информацию о таблицах через инспектор SQLAlchemy.

    Parameters:
    inspector (Any): объект-инспектор SQLAlchemy
    tables_names (Sequence[str]): имена таблиц
    title (Optional[str]): имя конкретной таблицы (если нужно получить только одну)

    Return:
    tables_info (Optional[Any]): информация о таблицах или None, если таблица не найдена
    """
    if title is None:
        return [
            {"_table_name": name, "column": format_columns(inspector.get_columns(name))}
            for name in tables_names
        ]
    else:
        if title in tables_names:
            return {
                "_table_name": title,
                "column": format_columns(inspector.get_columns(title)),
            }
        else:
            return None
