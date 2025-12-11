# FastAPI 관련 모듈 import
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db_dependency
from models import Question
from schemas import QuestionResponse, QuestionCreate
from typing import List
from datetime import datetime

# APIRouter 인스턴스 생성
router = APIRouter(
    prefix='/api/question'
)

# 질문 목록 조회 API
@router.get('/list', response_model=List[QuestionResponse])
def question_list(db: Session = Depends(get_db_dependency)):
    # 질문 조회
    question_list = db.query(Question).order_by(Question.create_date.desc()).all()
    return question_list

# 질문 등록 API
@router.post('/create', response_model=QuestionResponse)
def question_create(question_create: QuestionCreate, db: Session = Depends(get_db_dependency)):
    # 객체 생성
    new_question = Question(
        subject=question_create.subject,
        content=question_create.content,
        create_date=datetime.now()
    )

    # 디비에 추가
    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    return new_question