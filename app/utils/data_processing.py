"""
Документация модуля
"""

import re
import urllib.parse
import markdown2
from pathlib import Path
from typing import List, Optional

ANSWER_LINK_PREFIX = "[Ответ]("
ANSWER_LINK_SUFFIX = ")"
QUESTION_PATTERN = re.compile(
    r'### (?P<number_question>\d+).\s+(?P<question>.*?)'
    r'\s+(?P<trash>&nbsp;\s*)*<small>\[Ответ](?P<link>.*)</small>',
)
IGNORE_LINE_PREFIXES = ('<div', '[Вернуться к вопросам]', '</div', '\n')
CODEBLOCK_PYTHON = "```python"
CODEBLOCK = "```"


def decode_answer_link(line: str) -> str:
    """
    Извлекает и декодирует ссылку на файл-ответ из строки.
    """
    start = line.find(ANSWER_LINK_PREFIX) + len(ANSWER_LINK_PREFIX)
    end = line.find(ANSWER_LINK_SUFFIX, start)
    if start == -1 + len(ANSWER_LINK_PREFIX) or end == -1:
        raise ValueError("Невалидная строка со ссылкой ответа.")
    encoded_link = line[start:end]
    return urllib.parse.unquote(encoded_link)


def clean_answer_lines(lines: List[str]) -> str:
    """
    Очищает строки ответа от лишних разметок и объединяет их в одну строку.
    """
    filtered_lines = ""
    for line_2 in lines:
        if not line_2.strip().startswith(IGNORE_LINE_PREFIXES) and line_2:
            filtered_lines += line_2
    return filtered_lines


def convert_code_blocks(filtered_lines: str) -> str:
    """
    Преобразует markdown-код-блоки в html-вид для корректной обработки.
    """
    filtered_lines = re.sub(
        r'^(?P<indent>[ \t]*)```python',
        r'\g<indent><pre><code>',
        filtered_lines,
        flags=re.MULTILINE
    )
    filtered_lines = re.sub(
        r'^(?P<indent>[ \t]*)```',
        r'\g<indent></pre></code>',
        filtered_lines,
        flags=re.MULTILINE
    )

    return filtered_lines


def parse_answer_file(filepath: Path) -> str:
    """
    Читает файл-ответ, чистит лишние строки, форматирует code-блоки и превращает markdown в html.
    """
    with filepath.open(encoding='utf-8') as file:
        lines = file.readlines()

    filtered = clean_answer_lines(lines)
    html_convert = convert_code_blocks(filtered)
    return ''.join(markdown2.markdown(html_convert).strip())


def parse_question_file(
    question_path: Path = Path('app/doc/Список вопросов.txt'),
    answer_dir: Path = Path('app/doc/')
) -> List[List[Optional[str]]]:
    """
    Парсит файл вопросов, собирает вопросы, их тексты, html-ответы, и связанный блок кода (если есть).

    Возвращает список: [номер, текст вопроса, html-ответ, код (или None)]
    """
    questions: List[List[Optional[str]]] = []
    current: Optional[list] = None
    code_lines: Optional[List[str]] = None

    with question_path.open(encoding='utf-8') as file:
        for line in file:
            match = QUESTION_PATTERN.match(line)
            if match:
                if current:
                    if code_lines:
                        current[3] = "\n".join(code_lines)
                        code_lines = None
                    questions.append(current)

                number = int(match.group("number_question"))
                text = match.group("question").strip()
                answer_file = answer_dir / decode_answer_link(line.strip())
                html_answer = parse_answer_file(answer_file)
                current = [number, text, html_answer, None]
            elif current is not None:
                if line.startswith(CODEBLOCK) and code_lines is None:
                    code_lines = [line.rstrip("\n")]
                elif code_lines is not None:
                    code_lines.append(line.rstrip("\n"))
                    if line.strip() == CODEBLOCK:
                        current_code = '\n'.join(code_lines) + "\n```"
                        finish_current_code = convert_code_blocks(current_code)
                        current[3] = finish_current_code
                        code_lines = None

    if current:
        if code_lines:
            current[3] = "\n".join(code_lines)
        questions.append(current)

    return questions
