# FastAPI 관련 모듈 import
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db_dependency
from models import Question
from schemas import QuestionResponse
from typing import List

# APIRouter 인스턴스 생성
router = APIRouter(
    prefix='/api/question'
)

# 질문 목록 조회 API
@router.get('/list', response_model=List[QuestionResponse])
def question_list(db: Session = Depends(get_db_dependency)):
    # ORM을 이용해서 모든 질문을 조회
    question_list = db.query(Question).order_by(Question.create_date.desc()).all()
    return question_list