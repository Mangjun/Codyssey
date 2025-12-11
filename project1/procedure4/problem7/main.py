from fastapi import FastAPI
from database import engine
import models

# 데이터베이스 테이블 생성
models.Base.metadata.create_all(bind=engine)

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI()

# question 라우터 등록
from domain.question import question_router
app.include_router(question_router.router)

@app.get('/')
def main():
    return {'message': 'API 서버가 실행 중입니다.'}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)