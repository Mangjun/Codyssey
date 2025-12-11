from datetime import datetime
from database import SessionLocal, Base, engine
from models import Question

# 테이블 생성
Base.metadata.create_all(bind=engine)

# 더미 데이터 생성
dummy_questions = [
    {
        "subject": "FastAPI 설치 방법",
        "content": "FastAPI를 처음 설치하려고 하는데 어떻게 해야 하나요?",
        "create_date": datetime(2025, 12, 11, 10, 0, 0)
    },
    {
        "subject": "SQLAlchemy ORM 사용법",
        "content": "SQLAlchemy ORM을 사용해서 데이터베이스를 연결하고 싶습니다. 기본적인 사용법을 알려주세요.",
        "create_date": datetime(2025, 12, 11, 11, 30, 0)
    },
    {
        "subject": "Pydantic 스키마 정의하기",
        "content": "API 응답을 위한 Pydantic 스키마를 어떻게 정의하나요? 예제를 보여주세요.",
        "create_date": datetime(2025, 12, 11, 13, 15, 0)
    },
    {
        "subject": "contextlib 사용 목적",
        "content": "contextlib.contextmanager를 왜 사용하나요? 어떤 장점이 있는지 궁금합니다.",
        "create_date": datetime(2025, 12, 11, 14, 45, 0)
    },
    {
        "subject": "데이터베이스 연결 관리",
        "content": "데이터베이스 연결을 효율적으로 관리하는 방법이 있을까요? 연결 풀링에 대해서도 알고 싶습니다.",
        "create_date": datetime(2025, 12, 11, 16, 20, 0)
    }
]

# 세션 생성 및 데이터 삽입
db = SessionLocal()
try:
    print("더미 데이터 생성 시작...")

    # 기존 데이터 확인
    existing_count = db.query(Question).count()
    print(f"기존 질문 수: {existing_count}")

    if existing_count == 0:
        # 더미 데이터 삽입
        for question_data in dummy_questions:
            question = Question(**question_data)
            db.add(question)

        db.commit()
        print(f"{len(dummy_questions)}개의 더미 질문이 생성되었습니다.")
    else:
        print("이미 데이터가 존재하므로 더미 데이터를 추가하지 않습니다.")

    # 최종 데이터 확인
    total_count = db.query(Question).count()
    print(f"총 질문 수: {total_count}")

except Exception as e:
    print(f"오류 발생: {e}")
    db.rollback()
finally:
    db.close()
    print("데이터베이스 연결 종료")