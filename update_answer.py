"""
Модуль для обновления ответов в базе данных на основе файлов с ответами.
"""


from pathlib import Path
from sqlalchemy import create_engine, select, Column, Integer, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.utils.processing_data import extract_decode_answer_link, parse_answer_file
from app.config.config import POSTGRES_URL, QUESTION_PATTERN


class Base(DeclarativeBase):
    """
    Базовый класс для моделей SQLAlchemy.
    """


class Answers(Base):
    """
    Модель таблицы ответов.
    """

    __tablename__ = "answers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    answer = Column(String, nullable=False)
    question_id = Column(Integer)


def main(se: sessionmaker) -> None:
    """
    Обновляет ответы в базе данных на основе файлов с ответами.

    Parameters:
    se (sessionmaker): Фабрика сессий SQLAlchemy для работы с базой данных
    """
    question_path: Path = Path("app/doc/Список вопросов.txt")
    answer_dir: Path = Path("app/doc/")
    with se() as session:
        with question_path.open(encoding="utf-8") as file:
            for line in file:
                match = QUESTION_PATTERN.match(line)
                if match:
                    number: int = int(match.group("number_question"))
                    answer_file: Path = answer_dir / extract_decode_answer_link(
                        line.strip()
                    )
                    text_answer: str = parse_answer_file(answer_file)
                    stmt = select(Answers).where(Answers.id == number)
                    result = session.execute(stmt)
                    record = result.scalars().first()
                    if record:
                        record.answer = text_answer
        session.commit()


if __name__ == "__main__":
    engine = create_engine(POSTGRES_URL)
    Session = sessionmaker(engine)

    main(Session)
