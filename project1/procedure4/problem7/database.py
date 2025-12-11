from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

# 데이터베이스 설정
SQLALCHEMY_DATABASE_URL = 'sqlite:///./myapi.db'

# 데이터베이스 생성
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# contextlib을 이용한 데이터베이스 세션 관리
@contextmanager
def get_db_context():
    db = SessionLocal()
    try:
        print('데이터베이스 연결 시작')
        yield db
    finally:
        print('데이터베이스 연결 종료')
        db.close()

# contextlib을 이용한 get_db 함수
@contextmanager
def get_db():
    print('데이터베이스 연결 시작')
    db = SessionLocal()
    try:
        yield db
    finally:
        print('데이터베이스 연결 종료')
        db.close()

# Depends를 위한 래퍼 함수
def get_db_dependency():
    with get_db() as db:
        yield db