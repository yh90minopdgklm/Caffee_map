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

# ▲ 기본정보 확인 ▲
# ——————————————————————————————————————————————————————————————————


# struct 앞에 공백▼ 은 일부러 넣어놓으신 걸까? 이것 때문에 한참 에러났음
category_dict = pd.Series(df_category[' struct'].values, index = df_category['category']).to_dict()
# ID별 이름 매핑..
df_struct['category_name'] = df_struct['category'].map(category_dict)

print(df_struct[['x', 'y', 'category', 'category_name']].head(10))

merged_df = pd.merge(df_struct, df_map, on=['x','y'], how='left')
# ▲ df_struct 랑 df_map : x, y 기준으로 병합 ▲ 

# ——————————————————————————————————————————————————————————————————

sorted_df = merged_df.sort_values(by='area').reset_index(drop=True)
print(sorted_df.head())

# ▲ 정렬 및 출력 ▲ 
