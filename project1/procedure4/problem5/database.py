from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite 데이터베이스 파일 경로 설정
SQLALCHEMY_DATABASE_URL = 'sqlite:///./codyssey.db'

# SQLite 사용 시 check_same_thread 옵션이 필요함
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}
)

# 세션 생성 (autocommit=False, autoflush=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모델 정의를 위한 Base 클래스 생성
Base = declarative_base()