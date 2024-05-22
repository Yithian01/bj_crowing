import os
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
userId = ""

userId = input("백준 아이디를 입력해주세요 : ")


# 웹 드라이버 설정 (크롬 드라이버 경로를 지정하세요)
driver_path = 'path/to/chromedriver'
driver = webdriver.Chrome()
# 웹 페이지 열기
url = f'https://www.acmicpc.net/status?user_id={userId}&result_id=4'
driver.get(url)



# 데이터 저장용 리스트
data = []

# 무한 루프 돌면서 다음 페이지로 이동
while True:
    # 페이지 로드 대기
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    time.sleep(2)  # 페이지 로딩 시간을 위해 잠시 대기

    # 페이지 소스 가져오기
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # 데이터 파싱
    table_rows = soup.find_all('tr')  # 테이블 행 찾기
    for row in table_rows:
        columns = row.find_all('td')  # 테이블 데이터 찾기
        if len(columns) == 0:
            continue  # 헤더 행 건너뛰기
        row_data = [column.get_text(strip=True) for column in columns]
        data.append(row_data)
    
    # "제출한 시간"이 7개월인 항목이 있는지 확인
    stop_crawling = any('7달 전' in column.get_text(strip=True) for row in table_rows for column in row.find_all('td'))
    if stop_crawling:
        break

    # 다음 페이지 버튼 클릭
    try:
        next_button_xpath = '//*[@id="next_page"]'
        next_button = driver.find_element(By.XPATH, next_button_xpath )
        next_button.click()
    except Exception as e:
        print("다음 버튼을 찾을 수 없거나 클릭할 수 없습니다.", e)
        break

# 드라이버 종료
driver.quit()

# 데이터프레임 생성
columns = ['제출 번호', '아이디', '문제', '결과', '메모리', '시간', '언어', '코드 길이', '제출한 시간']
df = pd.DataFrame(data, columns=columns)

# 엑셀 파일로 저장
excel_file = f'tmp/new_crawled_data.xlsx'
df.to_excel(excel_file, index=False)
print(f"데이터가 '{excel_file}' 파일로 저장되었습니다.")




# 엑셀 파일 로드
file_path = 'tmp/new_crawled_data.xlsx'  # 엑셀 파일의 경로를 지정하세요
df = pd.read_excel(file_path)

# 중복된 '문제' 항목 제거 (첫 번째 항목만 남김)
df_unique = df.drop_duplicates(subset=['문제'])

# 결과를 새로운 엑셀 파일로 저장
output_file_path = f'data/{userId}_change_data.xlsx'
df_unique.to_excel(output_file_path, index=False)

print(f"중복된 항목이 제거된 파일이 '{output_file_path}'로 저장되었습니다.")

# tmp 폴더에 있는 파일 삭제
if os.path.exists(excel_file):
    os.remove(excel_file)
    print(f"'{excel_file}' 파일이 삭제되었습니다.")
else:
    print(f"'{excel_file}' 파일이 존재하지 않습니다.")

# 프로그램 종료
exit()