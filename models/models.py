"""
Документация модуля
"""

from sqlalchemy import create_engine, Column, Integer, String, select, exists, inspect
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config.config import DATABASE_URL
from utils.data_processing import parse_question_file

engine = create_engine(DATABASE_URL)


class Base(DeclarativeBase):
    pass


class Questions(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    add_question = Column(String)
    answer = Column(String)

    def __repr__(self):
        return f"<User(questions='{self.question}', add_question={self.add_question}, answer={self.answer})>"

    @classmethod
    def search_questions(cls, sesh) -> list:
        """
        ...

        Parameters:
        sesh (Session): Сессия SQLAlchemy для выполнения запроса.
        form (Form): Форма, содержащая данные для поиска строки.

        Return:
        ...
        """
        query = (
            select(Questions)
        )
        result = sesh.execute(query)
        all_books_objects = result.scalars().all()
        return all_books_objects


Session = sessionmaker(engine)
Base.metadata.create_all(engine)

with Session() as se:
    inspector = inspect(engine)
    table_exists = inspector.has_table('questions')
    data_exists = se.query(exists().where(Questions.id > 0)).scalar()
    if not table_exists or not data_exists:
        print("!!!!!")
        add_list = list()
        for data in parse_question_file():
            new_user = Questions(id=data[0], question=data[1], add_question=data[3], answer=data[2])
            add_list.append(new_user)
        se.add_all(add_list)
        se.commit()
