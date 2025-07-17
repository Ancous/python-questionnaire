"""
Модуль для обработки и парсинга файлов с вопросами и ответами.
Содержит функции для извлечения ссылок, фильтрации строк, парсинга файлов ответов и вопросов.
"""

import re
import urllib.parse
import markdown2
from pathlib import Path
from typing import List, Optional, Any

ANSWER_LINK_PREFIX = "[Ответ]("
ANSWER_LINK_SUFFIX = ")"
QUESTION_PATTERN = re.compile(
    r"### (?P<number_question>\d+).\s+(?P<question>.*?)"
    r"\s+(?P<trash>&nbsp;\s*)*<small>\[Ответ](?P<link>.*)</small>",
)
IGNORE_LINE_PREFIXES = ("<div", "[Вернуться к вопросам]", "</div", "\n")
CODEBLOCK = "```"


def extract_decode_answer_link(line: str) -> str:
    """
    Извлекает и декодирует ссылку на файл-ответ из строки.

    Parameters:
    line (str): строка, содержащая ссылку на ответ

    Return:
    decoded_link (str): декодированная ссылка на файл-ответ
    """
    start: int = line.find(ANSWER_LINK_PREFIX) + len(ANSWER_LINK_PREFIX)
    end: int = line.find(ANSWER_LINK_SUFFIX, start)
    if start == -1 + len(ANSWER_LINK_PREFIX) or end == -1:
        raise ValueError("Невалидная строка со ссылкой ответа.")
    encoded_link: str = line[start:end]
    return urllib.parse.unquote(encoded_link)


def filter_irrelevant_lines(lines: List[str]) -> str:
    """
    Очищает строки ответа от лишних разметок и объединяет их в одну строку.

    Parameters:
    lines (List[str]): список строк из файла ответа

    Return:
    filtered_lines (str): очищенный текст ответа одной строкой
    """
    filtered_lines: str = ""
    for line_2 in lines:
        if not line_2.strip().startswith(IGNORE_LINE_PREFIXES) and line_2:
            filtered_lines += line_2
    return filtered_lines


def parse_answer_file(filepath: Path) -> str:
    """
    Читает файл-ответ, чистит лишние строки, форматирует code-блоки и превращает markdown в html.

    Parameters:
    filepath (Path): путь к файлу-ответу

    Return:
    html (str): html-ответ
    """
    with filepath.open(encoding="utf-8") as file:
        lines: List[str] = file.readlines()

    filtered: str = filter_irrelevant_lines(lines)
    return markdown2.markdown(filtered, extras=["fenced-code-blocks"]).strip()


def parse_question_file(
    question_path: Path = Path("app/doc/Список вопросов.txt"),
    answer_dir: Path = Path("app/doc/"),
) -> List[List[Optional[str]]]:
    """
    Парсит файл вопросов, собирает вопросы, их тексты, html-ответы, и связанный блок кода (если есть).

    Parameters:
    question_path (Path): путь к файлу со списком вопросов
    answer_dir (Path): директория с файлами-ответами

    Return:
    questions (List[List[Optional[str]]]): список: [номер, текст вопроса, html-ответ, код (или None)]
    """
    questions: List[List[Optional[str]]] = []
    current: Optional[list] = None
    code_lines: Optional[List[str]] = None

    with question_path.open(encoding="utf-8") as file:
        for line in file:
            match = QUESTION_PATTERN.match(line)
            if match:
                if current:
                    if code_lines:
                        current[3] = "\n".join(code_lines)
                        code_lines = None
                    questions.append(current)

                number: int = int(match.group("number_question"))
                text: str = match.group("question").strip()
                answer_file: Path = answer_dir / extract_decode_answer_link(
                    line.strip()
                )
                html_answer: str = parse_answer_file(answer_file)
                current = [number, text, html_answer, None]
            elif current is not None:
                if line.startswith(CODEBLOCK) and code_lines is None:
                    code_lines = [line.rstrip("\n")]
                elif code_lines is not None:
                    code_lines.append(line.rstrip("\n"))
                    if line.strip() == CODEBLOCK:
                        current_code: str = "\n".join(code_lines)
                        current[3] = markdown2.markdown(
                            current_code, extras=["fenced-code-blocks"]
                        ).strip()
                        code_lines = None
    if current:
        if code_lines:
            current[3] = "\n".join(code_lines)
        questions.append(current)

    return questions
