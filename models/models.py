"""
Документация модуля
"""

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config.config import DATABASE_URL

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


Session = sessionmaker(engine)
Base.metadata.create_all(engine)
