import pandas as pd
import matplotlib.pyplot as plt

# 1단계에서 처리한 데이터 불러오기 (동일한 처리 과정)
df_category = pd.read_csv("dataFile/area_category.csv")
df_map = pd.read_csv("dataFile/area_map.csv")
df_struct = pd.read_csv("dataFile/area_struct.csv")

# 카테고리 매핑
category_dict = pd.Series(df_category[' struct'].values, index=df_category['category']).to_dict()
df_struct['category_name'] = df_struct['category'].map(category_dict)

# 데이터 병합
merged_df = pd.merge(df_struct, df_map, on=['x','y'], how='left')

# 데이터 확인: MyHome과 BandalgomCoffee 위치 찾기
print("=== 구조물 위치 분석 ===")
myhome_data = merged_df[merged_df['category_name'] == 'MyHome']
coffee_data = merged_df[merged_df['category_name'] == 'BandalgomCoffee']

print("MyHome 위치:")
print(myhome_data[['x', 'y', 'area']])
print("\nBandalgomCoffee 위치:")  
print(coffee_data[['x', 'y', 'area']])

# 모든 area 데이터 사용 (또는 필요한 구조물이 있는 area들만)
# area 1과 2를 모두 포함하거나, 전체 데이터 사용
df_filtered = merged_df.copy()  # 전체 데이터 사용

print(f"\n필터링된 데이터 개수: {len(df_filtered)}")
print(f"좌표 범위: x({df_filtered['x'].min()}~{df_filtered['x'].max()}), y({df_filtered['y'].min()}~{df_filtered['y'].max()})")
print(f"포함된 area: {sorted(df_filtered['area'].unique())}")

# 지도 크기 설정
x_min, x_max = df_filtered['x'].min(), df_filtered['x'].max()
y_min, y_max = df_filtered['y'].min(), df_filtered['y'].max()

# 플롯 생성
fig, ax = plt.subplots(figsize=(12, 10))

# 그리드 라인 그리기
for x in range(x_min, x_max + 1):
    ax.axvline(x=x, color='lightgray', linestyle='-', linewidth=0.5, alpha=0.7)
for y in range(y_min, y_max + 1):
    ax.axhline(y=y, color='lightgray', linestyle='-', linewidth=0.5, alpha=0.7)

# 구조물별 시각화
for _, row in df_filtered.iterrows():
    x, y = row['x'], row['y']
    category = row['category_name']
    
    if category == 'Apartment':
        # 갈색 원형
        ax.scatter(x, y, c='brown', s=100, marker='o', alpha=0.8, edgecolors='black', linewidth=1)
    elif category == 'Building':
        # 갈색 원형  
        ax.scatter(x, y, c='brown', s=100, marker='o', alpha=0.8, edgecolors='black', linewidth=1)
    elif category == 'BandalgomCoffee':
        # 녹색 사각형
        ax.scatter(x, y, c='green', s=150, marker='s', alpha=0.8, edgecolors='black', linewidth=1)
    elif category == 'MyHome':
        # 녹색 삼각형
        ax.scatter(x, y, c='green', s=150, marker='^', alpha=0.8, edgecolors='black', linewidth=1)

# 건설현장 따로 처리 (area_map.csv의 ConstructionSite=1인 곳)
construction_sites = merged_df[merged_df['ConstructionSite'] == 1]
for _, row in construction_sites.iterrows():
    x, y = row['x'], row['y']
    # 회색 사각형 (살짝 크게 만들어 겹치도록)
    ax.scatter(x, y, c='gray', s=200, marker='s', alpha=0.7, edgecolors='black', linewidth=1)

# 축 설정 (좌측 상단이 (1,1)이 되도록)
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_max, y_min)  # y축 뒤집기

# 축 레이블
#ax.set_xlabel('X', fontsize=12)
#ax.set_ylabel('Y', fontsize=12)
ax.set_title('Visualization', fontsize=14, fontweight='bold')

# 범례 추가 (보너스)
legend_elements = [
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='brown', 
               markersize=10, label='Apartment/Building', markeredgecolor='black'),
    plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='green', 
               markersize=10, label='BandalgomCoffee', markeredgecolor='black'),
    plt.Line2D([0], [0], marker='^', color='w', markerfacecolor='green', 
               markersize=10, label='MyHome', markeredgecolor='black'),
    plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='gray', 
               markersize=12, label='ConstructionSite', markeredgecolor='black', alpha=0.7)
]
ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.15, 1))

# 그리드 표시
ax.grid(True, alpha=0.3)
ax.set_aspect('equal')

# 이미지 저장
plt.tight_layout()
plt.savefig('map.png', dpi=300, bbox_inches='tight')
plt.close()

# 구조물별 개수 출력
structure_counts = df_filtered['category_name'].value_counts()
print("\n=== 구조물별 개수 ===")
for structure, count in structure_counts.items():
    print(f"{structure}: {count}개")

print(f"\n지도가 'map.png'로 저장되었습니다.")
