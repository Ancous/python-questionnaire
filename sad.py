"""
pass
"""

import re
from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.attributes import InstrumentedAttribute

from app.models.answer import Answers
from app.utils.processing_data import extract_decode_answer_link, parse_answer_file

POSTGRES_URL = "postgresql://root:1975@31.129.100.106:5432/python_interview"
QUESTION_PATTERN = re.compile(
    r'### (?P<number_question>\d+).\s+(?P<question>.*?)'
    r'\s+(?P<trash>&nbsp;\s*)*<small>\[Ответ](?P<link>.*)</small>',
)


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
                    answers_id: InstrumentedAttribute = Answers.id
                    stmt = select(Answers).where(answers_id == number)
                    result = session.execute(stmt)
                    record = result.scalars().first()
                    if record:
                        record.answer = text_answer
        session.commit()


if __name__ == '__main__':
    engine = create_engine(POSTGRES_URL)
    Session = sessionmaker(engine)
    main(Session)
