import requests
from bs4 import BeautifulSoup

def crawl_kbs_headlines():
    url = 'http://news.kbs.co.kr/news/pc/main/main.html'
    # 실제 브라우저처럼 보이게 하기 위한 User-Agent 헤더
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    headline_list = []

    try:
        # 헤더를 포함하여 웹 페이지의 HTML 소스를 가져옴
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')

        # === 변경된 부분 ===
        # 웹사이트 구조 변경에 따라 새로운 선택자로 수정
        # <p class="title">...</p> 형태의 모든 요소를 찾음
        headlines = soup.find_all('p', class_='title')
        # =================

        for headline in headlines:
            title = headline.get_text().strip()
            # 비어있지 않은 헤드라인만 리스트에 추가
            if title:
                headline_list.append(title)
            
        return headline_list

    except requests.exceptions.RequestException as e:
        print(f'오류: 웹 페이지를 가져오는 데 실패했습니다. (에러: {e})')
        return []
    except Exception as e:
        print(f'오류: 데이터를 처리하는 중 예외가 발생했습니다. (에러: {e})')
        return []

# --- 메인 실행 부분 ---
if __name__ == '__main__':
    print('KBS 뉴스 헤드라인을 가져오는 중입니다...')
    
    kbs_news = crawl_kbs_headlines()

    if kbs_news:
        print('\n--- [KBS 주요 뉴스] ---')
        for index, title in enumerate(kbs_news, 1):
            print(f'[{index}] {title}')
    else:
        print('뉴스를 가져오지 못했습니다.')