import csv
import os
from typing import List, Dict
from fastapi import FastAPI, APIRouter, HTTPException
# 수행과제 #7-1: model.py에서 TodoItem 임포트
from model import TodoItem 

# --- 1. 상수 및 전역 변수 설정 ---
CSV_FILE = 'todo.csv'
todo_list: List[Dict] = []


# --- 2. CSV 헬퍼 함수 (데이터 동기화용) ---
def read_csv_data() -> List[Dict]:
    """
    CSV_FILE에서 데이터를 읽어와 딕셔너리 리스트로 반환합니다.
    """
    data = []
    if not os.path.exists(CSV_FILE):
        return data
    try:
        with open(CSV_FILE, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
    except Exception as e:
        print(f'Error reading CSV file: {e}')
    return data


def write_csv_data(data: List[Dict]):
    """
    주어진 데이터를 CSV_FILE에 (덮어쓰기) 저장합니다.
    """
    if not data:
        open(CSV_FILE, 'w').close()
        return

    fieldnames = data[0].keys()
    try:
        with open(CSV_FILE, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    except Exception as e:
        print(f'Error writing to CSV file: {e}')


# --- 3. 데이터 처리를 위한 헬퍼 함수 ---
def find_todo_by_id(todo_id: str) -> (Dict | None, int):
    """
    전역 todo_list에서 id로 항목을 찾고 (항목, 인덱스)를 반환합니다.
    찾지 못하면 (None, -1)을 반환합니다.
    """
    for index, todo_item in enumerate(todo_list):
        # .get('id')를 사용해 'id' 키가 없는 경우에도 안전하게 처리
        if todo_item.get('id') == todo_id:
            return (todo_item, index)
    return (None, -1)


# --- 4. FastAPI 앱 및 APIRouter 설정 ---
app = FastAPI()
router = APIRouter()

# (핵심) 앱 시작 시 CSV에서 데이터를 읽어 전역 todo_list에 로드
todo_list = read_csv_data()


# --- 5. API 엔드포인트 정의 ---

# (기존) Create - POST
@router.post('/add_todo')
def add_todo(item: Dict) -> Dict:
    """
    todo_list에 새로운 항목을 추가합니다. (POST 방식)
    """
    if not item:
        return {'warning': 'Input dictionary is empty'}
    
    new_id = item.get('id')
    if not new_id:
        return {'warning': 'Input dictionary must have an "id"'}
        
    (found_item, _) = find_todo_by_id(new_id)
    if found_item:
        raise HTTPException(status_code=400, detail=f'Todo with id {new_id} already exists')

    todo_list.append(item)
    write_csv_data(todo_list)
    return {'message': 'Todo added successfully'}

# (기존) Retrieve All - GET
@router.get('/retrieve_todo')
def retrieve_todo() -> Dict:
    """
    todo_list 전체를 가져옵니다. (GET 방식)
    """
    return {'todos': todo_list}


# --- 수행과제 #1: 개별 조회 기능 ---
@router.get('/todo/{todo_id}')
def get_single_todo(todo_id: str) -> Dict:
    """
    경로 매개변수 {todo_id}를 이용해 개별 항목을 조회합니다. (GET 방식)
    """
    (found_item, _) = find_todo_by_id(todo_id)
    
    if not found_item:
        raise HTTPException(status_code=404, detail=f'Todo with id {todo_id} not found')
    
    return found_item


# --- 수행과제 #2: 수정 기능 ---
@router.put('/todo/{todo_id}')
def update_todo(todo_id: str, item_to_update: TodoItem) -> Dict:
    """
    {todo_id}로 항목을 찾아 TodoItem 모델의 내용으로 수정합니다. (PUT 방식)
    """
    (found_item, index) = find_todo_by_id(todo_id)
    
    if not found_item:
        raise HTTPException(status_code=404, detail=f'Todo with id {todo_id} not found')

    # (중요) 'task' 필드만 업데이트합니다. (id 등 다른 필드는 보존)
    found_item['task'] = item_to_update.task
    
    # 전역 리스트 업데이트
    todo_list[index] = found_item
    
    # CSV 파일에 저장
    write_csv_data(todo_list)
    
    return {'message': f'Todo {todo_id} updated successfully', 'item': found_item}


# --- 수행과제 #3: 삭제 기능 ---
@router.delete('/todo/{todo_id}')
def delete_single_todo(todo_id: str) -> Dict:
    """
    {todo_id}로 항목을 찾아 리스트에서 제거(삭제)합니다. (DELETE 방식)
    """
    (found_item, index) = find_todo_by_id(todo_id)
    
    if not found_item:
        raise HTTPException(status_code=404, detail=f'Todo with id {todo_id} not found')
        
    # 리스트에서 해당 인덱스 항목 제거
    deleted_item = todo_list.pop(index)
    
    # CSV 파일에 저장
    write_csv_data(todo_list)
    
    return {'message': f'Todo {todo_id} deleted successfully', 'item': deleted_item}


# 라우터를 메인 앱에 포함
app.include_router(router)