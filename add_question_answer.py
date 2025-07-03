"""
Документация модуля
"""

import re
import urllib.parse
import markdown2
from pathlib import Path
from typing import List, Optional

from sqlalchemy import create_engine, select, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase, relationship

POSTGRES_URL = "postgresql://root:1975@31.129.100.106:5432/python_interview"
ANSWER_LINK_PREFIX = "[Ответ]("
ANSWER_LINK_SUFFIX = ")"
QUESTION_PATTERN = re.compile(
    r'### (?P<number_question>\d+).\s+(?P<question>.*?)'
    r'\s+(?P<trash>&nbsp;\s*)*<small>\[Ответ](?P<link>.*)</small>',
)
IGNORE_LINE_PREFIXES = ('<div', '[Вернуться к вопросам]', '</div', '\n')
CODEBLOCK = "```"

finish_result = list()
add_questions = list()
add_answer = list()

engine = create_engine(POSTGRES_URL)
Session = sessionmaker(engine)


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
    question_id = Column(Integer, ForeignKey('questions.id'), unique=True, nullable=False)
    question = relationship(
        "Questions",
        back_populates="answer",
        uselist=False
    )


class Questions(Base):
    """
    Документация класса
    """
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(String, nullable=False)
    sub_question = Column(String)
    answer = relationship(
        "Answers",
        back_populates="question",
        uselist=False,
        cascade="all, delete-orphan"
    )


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
                answer_file = answer_dir / extract_decode_answer_link(line.strip())
                html_answer = parse_answer_file(answer_file)
                current = [number, text, html_answer, None]
            elif current is not None:
                if line.startswith(CODEBLOCK) and code_lines is None:
                    code_lines = [line.rstrip("\n")]
                elif code_lines is not None:
                    code_lines.append(line.rstrip("\n"))
                    if line.strip() == CODEBLOCK:
                        current_code = '\n'.join(code_lines)
                        current[3] = markdown2.markdown(current_code, extras=["fenced-code-blocks"]).strip()
                        code_lines = None

    if current:
        if code_lines:
            current[3] = "\n".join(code_lines)
        questions.append(current)

    return questions


def all_answer_db(se):
    """
    Документация функции
    """
    with se() as sess:
        stmt = select(Answers)
        itog = sess.execute(stmt)
        record = itog.scalars().all()

    return record


all_question = parse_question_file()
all_answer_db = all_answer_db(Session)

for obj_answer in all_answer_db:
    finish_result.append(obj_answer.answer)

with Session() as session:
    for question_data in all_question:
        if question_data[2] not in finish_result:
            new_questions = Questions(question=question_data[1], sub_question=question_data[3])
            new_answer = Answers(answer=question_data[2], question=new_questions)
            add_questions.append(new_questions)
            add_answer.append(new_answer)
    session.add_all(add_questions)
    session.add_all(add_answer)
    session.commit()
