import requests
import json
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

API_KEY = ""

start_year = 2015
end_year = 2024
start_month = 1
end_month = 12

def get_date(start_year, start_month, end_year, end_month):
    dates = []
    yyyy, mm = start_year, start_month

    while (yyyy, mm) <= (end_year, end_month):
        dates.append((yyyy, f"{mm:02d}"))
        if mm == 12:
            yyyy += 1
            mm = 1
        else:
            mm += 1
    return dates

responses = []

dates = get_date(start_year, start_month, end_year, end_month)
for year, month in dates:
    url = f"http://openapi.seoul.go.kr:8088/{API_KEY}/json/energyUseDataSummaryInfo/1/5/{year}/{month}"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        responses.append((year, month, data))
    except requests.exceptions.RequestException as e:
        print(f"API 호출 실패 ({year}-{month}): {e}")

# 최신 결과만 출력
if responses:
    year, month, latest_data = responses[-1]
    print("=== API 호출 결과 (최근 월만 출력)===")
    if 'energyUseDataSummaryInfo' in latest_data:
        block = latest_data['energyUseDataSummaryInfo']
        rows = block.get("row", [])
        print(f"연도-월: {year}-{month}")
        if rows:
            print("첫 번째 row 예시:")
            print(json.dumps(rows[0], ensure_ascii=False, indent=2))
        else:
            print("데이터 없음")
all_rows = []

for y, m, payload in responses:
    block = payload.get('energyUseDataSummaryInfo', {})
    rows = block.get('row', []) or []
    all_rows.extend(rows)

df = pd.DataFrame(all_rows)
print(df.info())
print(df.head(5).to_string(index=False))

df['date'] = pd.to_datetime(
    df['YEAR'].astype(str) + df['MON'].astype(str).str.zfill(2)+'01', format='%Y%m%d', errors = 'coerce'
)

df['year']  = df['date'].dt.year
df['month'] = df['date'].dt.month

spring = [3, 4, 5]
summer = [6, 7, 8]
fall = [9, 10, 11]
winter = [12, 1, 2]

df['season'] = df['month'].apply(
    lambda x: '봄' if x in spring
    else ('여름' if x in summer
    else ('가을' if x in fall else '겨울'))
)

print("계절 기본 정보 출력")
print(df.info())

print("변환 컬럼 확인")
cols_preview = ['YEAR', 'MON', 'MM_TYPE', 'date', 'year', 'month', 'season']
cols_preview = [c for c in cols_preview if c in df.columns]
print(df[cols_preview].head(10).to_string(index=False))

df_plot = df.copy()

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

energies = ['EUS', 'GUS', 'WUS', 'HUS']
for col in energies:
    df_plot[col] = pd.to_numeric(df_plot[col], errors='coerce')

season_order = ['봄', '여름', '가을', '겨울']
seasonal_gas_avg = df_plot.groupby('season')['GUS'].mean().reindex(season_order).reset_index()

plt.figure(figsize=(10, 6))

bars = plt.bar(seasonal_gas_avg['season'], seasonal_gas_avg['GUS'], color=['skyblue', 'lightgreen', 'gold', 'salmon'])

for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2.0,  
        height,                               
        f'{height:.0f}',                      
        ha='center',                          
        va='bottom',                         
        size=12
    )

plt.title('계절별 평균 가스 사용량', fontsize=16)
plt.xlabel('계절', fontsize=12)
plt.ylabel('평균 가스 사용량', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.ylim(0, seasonal_gas_avg['GUS'].max() * 1.15) 

plt.show()
plt.close()
print("계절별 평균 가스 사용량 데이터")
print(seasonal_gas_avg.to_string(index=False))
