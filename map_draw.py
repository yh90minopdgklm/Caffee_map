"""
2단계: 지도 시각화
반달곰 커피 프로젝트의 두 번째 단계로 분석된 데이터를 기반으로 지역 지도를 시각화합니다.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 한글 폰트 경고 방지 - 영어 폰트 사용
plt.rcParams['font.family'] = 'DejaVu Sans'


def load_processed_data():
    """
    1단계에서 처리된 데이터를 다시 불러오는 함수
    
    Returns:
        tuple: (처리된 데이터프레임, 카테고리 데이터프레임)
    """
    # CSV 파일들 불러오기
    area_map = pd.read_csv('area_map.csv')
    area_struct = pd.read_csv('area_struct.csv')
    area_category = pd.read_csv('area_category.csv')
    
    # 컬럼명과 데이터의 공백 제거
    area_category.columns = area_category.columns.str.strip()
    area_category['struct'] = area_category['struct'].str.strip()
    
    # 세 데이터를 하나의 DataFrame으로 병합
    merged_data = area_map.merge(area_struct, on=['x', 'y'], how='left')
    
    # area 1에 대한 데이터만 필터링
    area_1_data = merged_data[merged_data['area'] == 1].copy()
    
    # y좌표를 1부터 시작하도록 변환 (8→1, 9→2, ..., 15→8)
    area_1_data['y'] = area_1_data['y'] - 7
    
    return area_1_data, area_category


def create_map_visualization(data, category_df):
    """
    지도 시각화를 생성하는 함수
    
    Args:
        data (pandas.DataFrame): 시각화할 데이터프레임
        category_df (pandas.DataFrame): 카테고리 매핑 데이터프레임
    """
    # 좌표 범위 확인
    x_min, x_max = data['x'].min(), data['x'].max()
    y_min, y_max = data['y'].min(), data['y'].max()
    
    print(f'좌표 범위: x({x_min}-{x_max}), y({y_min}-{y_max})')
    
    # 그래프 설정
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # 좌표계 설정 (좌측 상단이 (1,1), 우측 하단이 최대값)
    ax.set_xlim(x_min - 0.5, x_max + 0.5)
    ax.set_ylim(y_min - 0.5, y_max + 0.5)  # y축 범위 설정
    ax.invert_yaxis()  # y축 뒤집기 (좌측 상단이 1,1)
    
    # 격자 라인 그리기
    for x in range(x_min, x_max + 1):
        ax.axvline(x, color='lightgray', linestyle='-', alpha=0.5)
    for y in range(y_min, y_max + 1):
        ax.axhline(y, color='lightgray', linestyle='-', alpha=0.5)
    
    # 카테고리 매핑
    category_mapping = category_df.set_index('category')['struct'].to_dict()
    
    # 구조물별 시각화 설정
    structure_colors = {
        'Apartment': 'brown',
        'Building': 'brown',
        'MyHome': 'green',
        'BandalgomCoffee': 'green'
    }
    
    structure_markers = {
        'Apartment': 'o',         # 원형
        'Building': 'o',          # 원형
        'MyHome': '^',            # 삼각형
        'BandalgomCoffee': 's'    # 사각형
    }
    
    structure_sizes = {
        'Apartment': 200,
        'Building': 200,
        'MyHome': 250,
        'BandalgomCoffee': 300
    }
    
    # 건설현장 시각화 (회색 사각형)
    construction_sites = data[data['ConstructionSite'] == 1]
    if not construction_sites.empty:
        ax.scatter(
            construction_sites['x'], 
            construction_sites['y'],
            c='gray',
            marker='s',
            s=400,
            alpha=0.8,
            edgecolors='black',
            linewidth=1,
            label='ConstructionSite'
        )
        print(f'건설현장 위치: {list(zip(construction_sites["x"], construction_sites["y"]))}')
    
    # 범례를 위한 핸들 저장
    legend_handles = []
    legend_labels = []
    
    # 구조물이 있는 좌표 시각화
    structures = data[data['category'] != 0]
    
    for category in structures['category'].unique():
        struct_name = category_mapping.get(category, f'Category_{category}')
        struct_data = structures[structures['category'] == category]
        
        scatter = ax.scatter(
            struct_data['x'], 
            struct_data['y'],
            c=structure_colors.get(struct_name, 'blue'),
            marker=structure_markers.get(struct_name, 'o'),
            s=structure_sizes.get(struct_name, 200),
            alpha=0.8,
            edgecolors='black',
            linewidth=1
        )
        
        # 범례용 핸들 저장
        legend_handles.append(scatter)
        legend_labels.append(struct_name)
        
        print(f'{struct_name} 위치: {list(zip(struct_data["x"], struct_data["y"]))}')
    
    # 축 설정 (영어로 변경하여 폰트 경고 방지)
    ax.set_xlabel('X Coordinate', fontsize=12)
    ax.set_ylabel('Y Coordinate', fontsize=12)
    ax.set_title('Bandalgom Coffee Area Map', fontsize=16, fontweight='bold')
    
    # 격자 눈금 설정
    ax.set_xticks(range(x_min, x_max + 1))
    ax.set_yticks(range(y_min, y_max + 1))
    
    # 보너스 확장: 범례 추가
    if legend_handles:
        ax.legend(
            legend_handles, 
            legend_labels, 
            loc='upper left', 
            bbox_to_anchor=(1.02, 1),
            fontsize=10,
            title='구조물 종류 (보너스 확장)'
        )
        print('\n=== 보너스 확장: 지도 범례 표시 완료 ===')
    
    # 그래프 조정
    plt.tight_layout()
    
    # 이미지 저장
    plt.savefig('map.png', dpi=300, bbox_inches='tight')
    print('지도가 map.png 파일로 저장되었습니다.')
    
    # 화면에 표시 (헤드리스 환경에서는 에러 발생 가능하지만 무시)
    try:
        plt.show()
    except:
        pass
    
    return fig, ax


def main():
    """
    메인 실행 함수
    """
    print('반달곰 커피 지도 시각화 프로젝트 - 2단계')
    print('=' * 50)
    
    # 데이터 불러오기
    data, category_df = load_processed_data()
    print(f'불러온 데이터 크기: {data.shape}')
    print()
    
    # 지도 시각화 생성
    create_map_visualization(data, category_df)
    
    print('2단계 지도 시각화 완료!')


if __name__ == '__main__':
    main()