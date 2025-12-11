# Pydantic 질문 스키마
from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional

# 질문 생성 스키마
class QuestionCreate(BaseModel):
    subject: str
    content: str

    @validator('subject')
    def subject_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('제목은 빈 값을 허용하지 않습니다')
        return v

    @validator('content')
    def content_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('내용은 빈 값을 허용하지 않습니다')
        return v

# 질문 응답 스키마
class QuestionResponse(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime

    class Config:
        from_attributes = True