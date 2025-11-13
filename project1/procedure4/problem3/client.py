import json
import urllib.request
import sys

BASE_URL = 'http://127.0.0.1:8000'

def _send_request(url, method='GET', data=None):
    """urllib.request를 사용해 API를 호출하는 헬퍼 함수"""
    
    # POST/PUT의 경우 데이터를 json.dumps로 직렬화
    json_data = None
    if data:
        json_data = json.dumps(data).encode('utf-8')

    try:
        req = urllib.request.Request(
            url, 
            data=json_data, 
            method=method,
            # JSON을 보낸다고 헤더에 명시
            headers={'Content-Type': 'application/json'} if json_data else {}
        )
        
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
            
    except urllib.error.HTTPError as e:
        # FastAPI가 404, 400 등을 반환하면 여기서 처리됨
        error_body = e.read().decode('utf-8')
        print(f"\n[오류 발생] (HTTP {e.code}): {json.loads(error_body)}")
        return None
    except urllib.error.URLError as e:
        print(f"\n[연결 실패] 서버가 실행 중인지 확인하세요. (Error: {e.reason})")
        # 서버가 안 켜져 있으면 프로그램 종료
        sys.exit(1)


# --- API 호출 함수들 ---

def get_all_todos():
    print('\n[전체 목록 조회]')
    result = _send_request(f'{BASE_URL}/retrieve_todo')
    if result and 'todos' in result:
        if not result['todos']:
            print(' -> 데이터가 없습니다.')
            return
        for todo in result['todos']:
            print(f" -> ID: {todo.get('id')}, Task: {todo.get('task')}")

def get_single_todo():
    todo_id = input('조회할 ID를 입력하세요: ')
    print(f'\n[ID {todo_id} 조회]')
    result = _send_request(f'{BASE_URL}/todo/{todo_id}')
    if result:
        print(f" -> ID: {result.get('id')}, Task: {result.get('task')}")

def add_todo():
    todo_id = input('추가할 ID를 입력하세요: ')
    task = input('추가할 Task를 입력하세요: ')
    
    new_data = {'id': todo_id, 'task': task}
    
    print(f'\n[ID {todo_id} 추가]')
    result = _send_request(f'{BASE_URL}/add_todo', method='POST', data=new_data)
    if result:
        print(f" -> {result.get('message') or result.get('warning')}")

def update_todo():
    todo_id = input('수정할 ID를 입력하세요: ')
    task = input('새로운 Task를 입력하세요: ')
    
    # model.py의 TodoItem(task=...) 형식에 맞춤
    update_data = {'task': task}
    
    print(f'\n[ID {todo_id} 수정]')
    result = _send_request(f'{BASE_URL}/todo/{todo_id}', method='PUT', data=update_data)
    if result:
        print(f" -> {result.get('message')}")

def delete_todo():
    todo_id = input('삭제할 ID를 입력하세요: ')
    print(f'\n[ID {todo_id} 삭제]')
    result = _send_request(f'{BASE_URL}/todo/{todo_id}', method='DELETE')
    if result:
        print(f" -> {result.get('message')}")

def main_menu():
    """메인 메뉴 루프"""
    print('='*30)
    print('FastAPI Todo 클라이언트 (urllib.request)')
    # 서버 연결 테스트 (최초 1회)
    _send_request(f'{BASE_URL}/retrieve_todo')
    print('[서버 연결 성공!]')
    print('='*30)

    while True:
        print('\n--- 메뉴 ---')
        print('1. 전체 목록 보기')
        print('2. 개별 항목 보기')
        print('3. 항목 추가')
        print('4. 항목 수정')
        print('5. 항목 삭제')
        print('6. 종료')
        choice = input('선택하세요 (1-6): ')
        
        if choice == '1':
            get_all_todos()
        elif choice == '2':
            get_single_todo()
        elif choice == '3':
            add_todo()
        elif choice == '4':
            update_todo()
        elif choice == '5':
            delete_todo()
        elif choice == '6':
            print('클라이언트를 종료합니다.')
            break
        else:
            print('잘못된 입력입니다. 1~6 사이의 숫자를 입력하세요.')

if __name__ == '__main__':
    main_menu()