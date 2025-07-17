"""
Модуль для агрегации статистических данных.
Содержит функцию для группировки и преобразования результатов статистики в удобный для анализа вид.
"""

from collections import defaultdict
from typing import Any, Dict, List, Tuple, Iterable


def statistic_data(
    results: Iterable[Tuple[Any, Any, Any]]
) -> dict[Any, List[Tuple[Any, Any]]]:
    """
    Группирует и преобразует результаты статистики в удобный для анализа вид.

    Parameters:
    results (Iterable[Tuple[Any, Any, Any]]): результаты статистики (кортежи из трёх элементов)

    Return:
    data (dict[Any, List[Tuple[Any, Any]]]): сгруппированные данные по первому полю
    """
    grouped: Dict[Any, List[Tuple[Any, Any]]] = defaultdict(list)
    for field1, field2, field3 in results:
        grouped[field1].append((field2, field3))
    data: dict[Any, List[Tuple[Any, Any]]] = dict(grouped)
    return data
