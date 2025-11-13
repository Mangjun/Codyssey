from pydantic import BaseModel

# 수행과제 #7-2: BaseModel을 상속받는 TodoItem 모델
class TodoItem(BaseModel):
    task: str