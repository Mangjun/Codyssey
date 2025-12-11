# Pydantic 질문 스키마
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# 질문 응답 스키마
class QuestionResponse(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime

    class Config:
        from_attributes = True