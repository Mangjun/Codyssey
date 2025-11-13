import csv
import os
from typing import List, Dict
from fastapi import FastAPI, APIRouter, HTTPException

# --- 1. 상수 및 전역 변수 설정 ---

# 제약조건 #3: CSV 파일을 사용
CSV_FILE = 'todo.csv'

# 수행과제 #5: 리스트 객체 'todo_list'
# (시작 시 CSV 파일로부터 데이터를 읽어와 채웁니다)
todo_list: List[Dict] = []


# --- 2. CSV 헬퍼 함수 (데이터 동기화용) ---

def read_csv_data() -> List[Dict]:
    """
    CSV_FILE에서 데이터를 읽어와 딕셔너리 리스트로 반환합니다.
    파일이 없으면 빈 리스트를 반환합니다.
    """
    data = []
    if not os.path.exists(CSV_FILE):
        return data  # 파일이 없으면 빈 리스트 반환
    
    try:
        with open(CSV_FILE, 'r', encoding='utf-8', newline='') as f:
            # csv.DictReader를 사용해 딕셔너리로 읽어들임
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
    except Exception as e:
        print(f'Error reading CSV file: {e}')
    
    return data


def write_csv_data(data: List[Dict]):
    """
    주어진 데이터를 CSV_FILE에 (덮어쓰기) 저장합니다.
    데이터가 비어있으면 헤더만 쓰거나 빈 파일을 만듭니다.
    """
    if not data:
        # 데이터가 없으면 빈 파일로 덮어씀
        open(CSV_FILE, 'w').close()
        return

    # 첫 번째 아이템의 키를 헤더(fieldnames)로 사용
    fieldnames = data[0].keys()
    
    try:
        with open(CSV_FILE, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()  # 헤더 쓰기
            writer.writerows(data)  # 모든 데이터 쓰기
    except Exception as e:
        print(f'Error writing to CSV file: {e}')


# --- 3. FastAPI 앱 및 APIRouter 설정 ---

app = FastAPI()
router = APIRouter()

# (핵심) 앱 시작 시 CSV에서 데이터를 읽어 전역 todo_list에 로드
todo_list = read_csv_data()


# --- 4. API 엔드포인트 정의 (수행과제 #6) ---

@router.post('/add_todo')
def add_todo(item: Dict) -> Dict:
    """
    수행과제 #6-1: todo_list에 새로운 항목을 추가합니다.
    (POST 방식, 입출력 Dict)
    """
    
    # 보너스 과제: 입력된 Dict가 빈 값인지 확인
    if not item:
        # 400 Bad Request를 반환하는 것이 RESTful하지만,
        # "경고를 돌려준다"는 요구사항에 맞춰 200 OK와 함께 경고 메시지 반환
        return {'warning': 'Input dictionary is empty'}

    # 1. 메모리(todo_list)에 추가
    todo_list.append(item)
    
    # 2. CSV 파일에 변경 사항 저장 (동기화)
    write_csv_data(todo_list)
    
    return {'message': 'Todo added successfully'}


@router.get('/retrieve_todo')
def retrieve_todo() -> Dict:
    """
    수행과제 #6-2: todo_list를 가져옵니다.
    (GET 방식, 입출력 Dict)
    """
    
    # "입출력은 Dict 타입" 요구사항을 맞추기 위해 리스트를 딕셔너리로 감싸서 반환
    return {'todos': todo_list}


# 라우터를 메인 앱에 포함
app.include_router(router)