import requests
from bs4 import BeautifulSoup

def crawl_stock_index():
    url = 'https://finance.naver.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        # 지수 정보가 들어있는 <dl class="blind"> 태그를 찾음
        index_container = soup.find('dl', class_='blind')
        
        if index_container:
            # <dl> 태그 안의 모든 <dd> 태그를 리스트로 가져옴
            dd_list = index_container.find_all('dd')
            
            # dd_list[0] -> 날짜 정보
            # dd_list[1] -> 코스피 정보
            # dd_list[2] -> 코스닥 정보
            
            # strip()으로 양쪽 공백 제거
            kospi_text = dd_list[1].get_text(strip=True)
            kosdaq_text = dd_list[2].get_text(strip=True)
            
            print(f"📈 {kospi_text}")
            print(f"📉 {kosdaq_text}")

        else:
            print('지수 정보를 담고 있는 컨테이너를 찾을 수 없습니다.')
            
    except Exception as e:
        print(f'오류: 지수 정보를 가져오는 데 실패했습니다. (에러: {e})')

# --- 메인 실행 부분 ---
if __name__ == '__main__':
    crawl_stock_index()