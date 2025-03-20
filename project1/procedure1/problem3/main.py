import csv

# 임시 저장소
data = list()

try :
    # csv 파일 읽기
    f = open('Mars_Base_Inventory_List.csv', 'r', encoding='utf-8')
    reader = csv.reader(f)

    print("Mars_Base_Inventory_List.csv 읽었습니다.")
    print()

    # csv 파일 출력
    for row in reader :
        print(row[0], row[1], row[2], row[3], row[4])
        data.append((row[0], row[1], row[2], row[3], row[4]))

    print()
    
    # 인화성 지수가 0.7 이상되는 목록을 저장할 csv 파일
    new_file = open('Mars_Base_Inventory_danger.csv', 'w', encoding='utf-8', newline='')
    writer = csv.writer(new_file)

    # 인화성이 높은 순으로 정렬
    sort_list = sorted(data[1:], key=lambda x: x[4], reverse=True)

    # 헤더 추가
    sort_list.insert(0, data[0])
    
    # 인화성 0.7 이상인 목록
    danger_list = list()
    danger_list.append(data[0])

    print("인화성이 0.7 이상인 목록 출력합니다.")
    print()

    # 인화성이 0.7 이상인 목록 출력
    for row in sort_list :
        if row[4] >= '0.7' :
            print(row[0], row[1], row[2], row[3], row[4])
            danger_list.append((row[0], row[1], row[2], row[3], row[4]))

    print()

    # 인화성이 0.7 이상인 목록 csv 파일로 저장
    writer.writerows(danger_list)

    # (보너스 과제) 이진 파일로 저장
    binary_file = open('Mars_Base_Inventory_List.bin', 'wb')
    binary_file.write(bytes(str(sort_list), 'utf-8'))

    '''
    텍스트 파일의 장단점
    
    장점
    1. 사람이 읽기 쉽고 수정하기 쉽다.
    2. 다양한 프로그램과 운영체제에서 쉽게 사용 가능하다.
    3. 데이터가 구조화되어 있어 처리하기 쉽다.

    단점
    1. 파일 크기가 크다.
    2. 저장 형식이 일정하지 않으면 파싱(읽기)하기 어렵다.
    3. 속도가 느리다.

    이진 파일의 장단점
    
    장점
    1. 파일 크기가 작다.
    2. 속도가 빠르다.
    3. 복잡한 데이터 구조가 저장이 가능하다.

    단점
    1. 사람이 직접 읽거나 수정하기 어렵다.
    2. 특정 프로그램이나 라이브러리가 필요할 수 있다.
    3. 다른 운영체제에서 호환되지 않을 수 있다.

    텍스트 파일과 이진 파일의 차이점
    데이터 저장 방식 : 텍스트 파일은 문자 형태로 저장하고, 이진 파일은 0과 1로 저장한다.
    파일 확장자 : 텍스트 파일은 .txt, .csv 등이 있고, 이진 파일은 .bin, .dat 등이 있다.
    '''

    # 파일 리소스 회수
    f.close()
    new_file.close()
    binary_file.close()
except FileNotFoundError :
    print("File not found")