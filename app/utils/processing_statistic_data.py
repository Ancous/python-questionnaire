"""
Документация модуля
"""

from collections import defaultdict


def statistic_data(results) -> dict:
    """
    Документация функции
    """
    grouped = defaultdict(list)
    for field1, field2, field3 in results:
        grouped[field1].append((field2, field3))
    data = dict(grouped)
    return data
