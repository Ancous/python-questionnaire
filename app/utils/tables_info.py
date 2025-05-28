"""
Документация модуля
"""


def format_columns(columns):
    """
    Документация функции
    """
    result = []
    for column in columns:
        column.pop("default", None)
        column.pop("comment", None)
        column["type"] = str(column["type"])
        result.append(column)
    return result


def inspector_tables(inspector, tables_names, title=None):
    """
    Документация функции
    """
    if title is None:
        return [
            {
                "_table_name": name,
                "column": format_columns(inspector.get_columns(name))
            }
            for name in tables_names
        ]
    else:
        if title in tables_names:
            return {
                "_table_name": title,
                "column": format_columns(inspector.get_columns(title))
            }
        else:
            return None
