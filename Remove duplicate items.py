import pandas as pd

# 엑셀 파일 로드
file_path = 'bj_crawled_data.xlsx'  # 엑셀 파일의 경로를 지정하세요
df = pd.read_excel(file_path)

# 중복된 '문제' 항목 제거 (첫 번째 항목만 남김)
df_unique = df.drop_duplicates(subset=['문제'])

# 결과를 새로운 엑셀 파일로 저장
output_file_path = 'change_data.xlsx'
df_unique.to_excel(output_file_path, index=False)

print(f"중복된 항목이 제거된 파일이 '{output_file_path}'로 저장되었습니다.")
