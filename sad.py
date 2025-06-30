"""
pass
"""

import re
from pathlib import Path
import urllib.parse
from typing import List

import markdown2
from sqlalchemy import create_engine, select, Column, Integer, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase

POSTGRES_URL = "postgresql://root:1975@31.129.100.106:5432/python_interview"
QUESTION_PATTERN = re.compile(
    r'### (?P<number_question>\d+).\s+(?P<question>.*?)'
    r'\s+(?P<trash>&nbsp;\s*)*<small>\[Ответ](?P<link>.*)</small>',
)
ANSWER_LINK_PREFIX = "[Ответ]("
ANSWER_LINK_SUFFIX = ")"
IGNORE_LINE_PREFIXES = ('<div', '[Вернуться к вопросам]', '</div', '\n')


class Base(DeclarativeBase):
    """
    Документация класса
    """
    pass


class Answers(Base):
    """
    Документация класса
    """
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    answer = Column(String, nullable=False)
    question_id = Column(Integer)


def filter_irrelevant_lines(lines: List[str]) -> str:
    """
    Очищает строки ответа от лишних разметок и объединяет их в одну строку.
    """
    filtered_lines = ""
    for line_2 in lines:
        if not line_2.strip().startswith(IGNORE_LINE_PREFIXES) and line_2:
            filtered_lines += line_2
    return filtered_lines


def parse_answer_file(filepath: Path) -> str:
    """
    Читает файл-ответ, чистит лишние строки, форматирует code-блоки и превращает markdown в html.
    """
    with filepath.open(encoding='utf-8') as file:
        lines = file.readlines()

    filtered = filter_irrelevant_lines(lines)
    return markdown2.markdown(filtered, extras=["fenced-code-blocks"]).strip()


def extract_decode_answer_link(line: str) -> str:
    """
    Извлекает и декодирует ссылку на файл-ответ из строки.
    """
    start = line.find(ANSWER_LINK_PREFIX) + len(ANSWER_LINK_PREFIX)
    end = line.find(ANSWER_LINK_SUFFIX, start)
    if start == -1 + len(ANSWER_LINK_PREFIX) or end == -1:
        raise ValueError("Невалидная строка со ссылкой ответа.")
    encoded_link = line[start:end]
    return urllib.parse.unquote(encoded_link)


def main(se):
    """
    Документация функции
    """
    question_path: Path = Path('app/doc/Список вопросов.txt')
    answer_dir: Path = Path('app/doc/')
    with se() as session:
        with question_path.open(encoding='utf-8') as file:
            for line in file:
                match = QUESTION_PATTERN.match(line)
                if match:
                    number = int(match.group("number_question"))
                    answer_file = answer_dir / extract_decode_answer_link(line.strip())
                    text_answer = parse_answer_file(answer_file)
                    stmt = select(Answers).where(Answers.id == number)
                    result = session.execute(stmt)
                    record = result.scalars().first()
                    if record:
                        record.answer = text_answer
        session.commit()


if __name__ == '__main__':
    engine = create_engine(POSTGRES_URL)
    Session = sessionmaker(engine)
    main(Session)
