import pandas as pd
import matplotlib.pyplot as plt

# output 보기 안좋음
# —————————————————————————————————

def load_data(csv_file):
    """CSV 파일에서 데이터 로드"""
    df = pd.read_csv(csv_file)
    
    # 데이터 구조화
    locations = {
        'Apartment': [],
        'Building': [],
        'BandalgomCoffee': [],
        'MyHome': [],
        'ConstructionSite': []
    }
    
    # 각 유형별 좌표 분류
    for _, row in df.iterrows():
        category = row['category']
        x, y = float(row['x']), float(row['y'])
        locations[category].append((x, y))
    
    return locations

def visualize_map(data, filename='map.png'):
    """지도 시각화 함수"""
    # 최대 좌표 계산
    max_x = max(max(x for x, y in coords) for coords in data.values())
    max_y = max(max(y for x, y in coords) for coords in data.values())

    # 플롯 설정
    plt.figure(figsize=(15, 15))
    ax = plt.gca()
    
    # 그리드 라인 추가
    ax.grid(True, linestyle='-', alpha=0.3)
    
    # 각 유형별 마커 스타일 정의
    markers = {
        'Apartment': ('o', '#CD853F'),      # 갈색 원형
        'Building': ('o', '#CD853F'),         # 갈색 원형
        'BandalgomCoffee': ('s', '#228B22'), # 녹색 사각형
        'MyHome': ('^', '#228B22'),       # 녹색 삼각형
        'ConstructionSite': ('s', '#808080')     # 회색 사각형
    }
    
    # 건설 현장을 제외한 모든 시설 그리기
    for category, coords in data.items():
        if category != 'ConstructionSite':
            x_coords, y_coords = zip(*coords)
            ax.scatter(x_coords, y_coords, marker=markers[category][0], 
                      c=markers[category][1], label=category, zorder=1, s=2000)
    
    # 건설 현장 그리기 (겹침 허용)
    x_coords, y_coords = zip(*data['ConstructionSite'])
    ax.scatter(x_coords, y_coords, marker='s', c='#808080', 
              label='ConstructionSite', zorder=2, s=3000)
    
    # 범례와 제목 추가
#    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
#    plt.title('Visualization')
    
    # 축 설정
    ax.set_xlim(1, max_x)
    ax.set_ylim(1, max_y)
    ax.invert_yaxis()  # 좌상단이 (1,1)이 되도록 y축 반전
    
    # 파일 저장
    plt.savefig(filename, bbox_inches='tight', dpi=300)
    plt.close()

def main():
    """메인 실행 함수"""
    csv_file = 'location_data.csv'  # CSV 파일 경로
    data = load_data(csv_file)
    visualize_map(data)

if __name__ == '__main__':
    main()