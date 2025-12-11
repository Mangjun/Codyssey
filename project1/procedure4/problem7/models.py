from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base

class Question(Base):
    __tablename__ = 'question'

    # PK
    id = Column(Integer, primary_key=True)
    # 질문 제목
    subject = Column(String, nullable=False)
    # 질문 내용
    content = Column(Text, nullable=False)
    # 질문 작성일시
    create_date = Column(DateTime, nullable=False)