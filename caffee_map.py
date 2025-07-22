import pandas as pd
df_category  = pd.read_csv("dataFile/area_category.csv")
df_map = pd.read_csv("dataFile/area_map.csv")
df_struct = pd.read_csv("dataFile/area_struct.csv")

print(df_category.head())
print(df_category.columns)
print(df_map.head())
print(df_map.columns)
print(df_struct.head())
print(df_struct.columns)
# 1. 기본정보 확인 ▲
# ——————————————————————————————————————————————————————————————————


# struct 앞에 공백▼ 은 일부러 넣어놓으신 걸까? 이것 때문에 한참 에러났음
category_dict = pd.Series(df_category[' struct'].values, index = df_category['category']).to_dict()
# ID별 이름 매핑..
df_struct['category_name'] = df_struct['category'].map(category_dict)

print(df_struct[['x', 'y', 'category', 'category_name']].head(10))

merged_df = pd.merge(df_struct, df_map, on=['x','y'], how='left')
# 2. df_struct 랑 df_map : x, y 기준으로 병합 ▲ 

# ——————————————————————————————————————————————————————————————————

sorted_df = merged_df.sort_values(by='area').reset_index(drop=True)
print(sorted_df)

# 3. 정렬 및 출력 ▲ 
# ——————————————————————————————————————————————————————————————————

df2 = sorted_df.loc[sorted_df['area'] == 1]
print(df2)

# 4. 필터링 ▲ 
# * 1~3까지는 조금 헷갈렸으나 4는 비교적 무난했다.
# ——————————————————————————————————————————————————————————————————

summary = (
    df_struct.groupby('category_name')
    .agg(
        구조물_수 = ('category', 'count'),
        area_Average = ('area', 'mean'),
        area_Min = ('area', 'min'),
        area_Max = ('area', 'max')
    )
    .reset_index()
)
print(summary)

# 보너스. 구조물 종류별 그룹 집계 (groupby 사용) ▲ 
# ——————————————————————————————————————————————————————————————————
