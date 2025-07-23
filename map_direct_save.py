"""
3단계: 최단경로 찾기 (BFS 알고리즘)
반달곰 커피 프로젝트의 세 번째 단계로 BFS를 이용해 MyHome에서 BandalgomCoffee까지의 최단경로를 찾습니다.
"""

import pandas as pd
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 한글 폰트 경고 방지 - 영어 폰트 사용
plt.rcParams['font.family'] = 'DejaVu Sans'


def load_processed_data():
    """
    전체 데이터를 불러오는 함수 (MyHome 위치 포함)
    
    Returns:
        tuple: (전체 데이터프레임, 카테고리 데이터프레임)
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
    
    # Y좌표는 원본 그대로 사용 (1~15 범위)
    
    # 전체 데이터 사용 (area 필터링 제거)
    print(f'전체 데이터 크기: {merged_data.shape}')
    
    return merged_data, area_category


def find_start_and_end_points(data, category_df):
    """
    시작점과 끝점(BandalgomCoffee)을 찾는 함수
    
    Args:
        data (pandas.DataFrame): 데이터프레임
        category_df (pandas.DataFrame): 카테고리 매핑 데이터프레임
        
    Returns:
        tuple: (시작점 좌표, 끝점 좌표)
    """
    # 카테고리 매핑
    category_mapping = category_df.set_index('category')['struct'].to_dict()
    reverse_mapping = {v: k for k, v in category_mapping.items()}
    
    # MyHome 찾기 - 전체 데이터에서 찾기
    home_category = reverse_mapping.get('MyHome')
    home_data_full = data[data['category'] == home_category]
    
    # BandalgomCoffee 찾기 - 전체 데이터에서 찾기
    cafe_category = reverse_mapping.get('BandalgomCoffee')
    cafe_data_full = data[data['category'] == cafe_category]
    
    if cafe_data_full.empty:
        print('경고: BandalgomCoffee를 찾을 수 없습니다.')
        return None, None
    
    if not home_data_full.empty:
        # 전체 데이터에서 MyHome 발견 - 실제 위치 사용
        start_point = (int(home_data_full.iloc[0]['x']), int(home_data_full.iloc[0]['y']))
        print(f'MyHome 실제 위치: {start_point}')
    else:
        print('경고: MyHome을 찾을 수 없습니다.')
        return None, None
    
    # 첫 번째 카페 위치를 목적지로 사용
    end_point = (int(cafe_data_full.iloc[0]['x']), int(cafe_data_full.iloc[0]['y']))
    
    print(f'시작점: {start_point}')
    print(f'목적지 (BandalgomCoffee): {end_point}')
    
    return start_point, end_point


def create_grid_map(data, start_point=None):
    """
    BFS를 위한 격자 지도를 생성하는 함수
    
    Args:
        data (pandas.DataFrame): 데이터프레임
        start_point (tuple): 시작점 좌표 (격자 맵에 추가할 경우)
        
    Returns:
        dict: {(x, y): '장애물여부'} 형태의 격자 지도
    """
    grid_map = {}
    
    for _, row in data.iterrows():
        x, y = int(row['x']), int(row['y'])
        
        # 건설현장은 장애물
        if row['ConstructionSite'] == 1:
            grid_map[(x, y)] = 'obstacle'
        # Apartment와 Building도 장애물
        elif row['category'] in [1, 2]:  # 1: Apartment, 2: Building
            grid_map[(x, y)] = 'obstacle'
        else:
            grid_map[(x, y)] = 'free'
    
    # 시작점이 격자 맵에 없다면 추가 (MyHome이 area 1 외부에 있는 경우)
    if start_point and start_point not in grid_map:
        grid_map[start_point] = 'free'
        print(f'시작점 {start_point}을 격자 맵에 추가했습니다.')
    
    return grid_map


def bfs_shortest_path(grid_map, start, end):
    """
    BFS 알고리즘을 이용해 최단경로를 찾는 함수
    
    Args:
        grid_map (dict): 격자 지도
        start (tuple): 시작점 좌표
        end (tuple): 끝점 좌표
        
    Returns:
        list: 최단경로 좌표 리스트
    """
    # BFS 초기화
    queue = deque([(start, [start])])
    visited = {start}
    
    # 4방향 이동 (상, 하, 좌, 우)
    directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
    
    while queue:
        (current_x, current_y), path = queue.popleft()
        
        # 목적지에 도달한 경우
        if (current_x, current_y) == end:
            print(f'최단경로 발견! 경로 길이: {len(path)}')
            return path
        
        # 4방향으로 이동 시도
        for dx, dy in directions:
            next_x, next_y = current_x + dx, current_y + dy
            next_pos = (next_x, next_y)
            
            # 이미 방문했거나 격자 범위를 벗어난 경우 무시
            if next_pos in visited or next_pos not in grid_map:
                continue
            
            # 장애물인 경우 무시
            if grid_map[next_pos] == 'obstacle':
                continue
            
            # 방문 처리 및 큐에 추가
            visited.add(next_pos)
            new_path = path + [next_pos]
            queue.append((next_pos, new_path))
    
    print('경로를 찾을 수 없습니다.')
    return []


def visualize_path(data, category_df, path, start, end):
    """
    경로를 시각화하는 함수
    
    Args:
        data (pandas.DataFrame): 데이터프레임
        category_df (pandas.DataFrame): 카테고리 데이터프레임
        path (list): 경로 좌표 리스트
        start (tuple): 시작점
        end (tuple): 끝점
    """
    # 좌표 범위 확인
    x_min, x_max = data['x'].min(), data['x'].max()
    y_min, y_max = data['y'].min(), data['y'].max()
    
    # 그래프 설정
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # 좌표계 설정
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
        'Apartment': 'o',
        'Building': 'o',
        'MyHome': '^',
        'BandalgomCoffee': 's'
    }
    
    structure_sizes = {
        'Apartment': 200,
        'Building': 200,
        'MyHome': 250,
        'BandalgomCoffee': 300
    }
    
    # 건설현장 시각화
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
    
    # 구조물 시각화
    structures = data[data['category'] != 0]
    for category in structures['category'].unique():
        struct_name = category_mapping.get(category, f'Category_{category}')
        struct_data = structures[structures['category'] == category]
        
        ax.scatter(
            struct_data['x'], 
            struct_data['y'],
            c=structure_colors.get(struct_name, 'blue'),
            marker=structure_markers.get(struct_name, 'o'),
            s=structure_sizes.get(struct_name, 200),
            alpha=0.8,
            edgecolors='black',
            linewidth=1,
            label=struct_name
        )
    
    # 경로 시각화
    if path:
        path_x = [point[0] for point in path]
        path_y = [point[1] for point in path]
        
        # 경로 선 그리기
        ax.plot(path_x, path_y, 'r-', linewidth=3, alpha=0.7, label='Shortest Path')
        
        # 경로 점들 표시
        ax.scatter(path_x, path_y, c='red', s=50, alpha=0.7, zorder=5)
        
        # 시작점과 끝점 강조
        ax.scatter(start[0], start[1], c='blue', s=400, marker='*', 
                  edgecolors='black', linewidth=2, label='Start', zorder=6)
        ax.scatter(end[0], end[1], c='red', s=400, marker='*', 
                  edgecolors='black', linewidth=2, label='End', zorder=6)
    
    # 축 설정
    ax.set_xlabel('X Coordinate', fontsize=12)
    ax.set_ylabel('Y Coordinate', fontsize=12)
    ax.set_title('Coffee Map with Shortest Path', fontsize=16, fontweight='bold')
    
    # 격자 눈금 설정
    ax.set_xticks(range(x_min, x_max + 1))
    ax.set_yticks(range(y_min, y_max + 1))
    
    # 범례 추가
    ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1), fontsize=10)
    
    # 그래프 조정
    plt.tight_layout()
    
    # 이미지 저장
    plt.savefig('map_final.png', dpi=300, bbox_inches='tight')
    print('최단경로가 포함된 지도가 map_final.png 파일로 저장되었습니다.')
    
    # 화면에 표시
    try:
        plt.show()
    except:
        pass


def save_path_to_csv(path):
    """
    경로를 CSV 파일로 저장하는 함수
    
    Args:
        path (list): 경로 좌표 리스트
    """
    if not path:
        print('저장할 경로가 없습니다.')
        return
    
    # DataFrame 생성 (step, x, y 순서)
    path_df = pd.DataFrame({
        'x': [point[0] for point in path],
        'y': [point[1] for point in path],
        'step': range(1, len(path) + 1)
    })
    
    # 컬럼 순서 조정
    path_df = path_df[['step', 'x', 'y']]
    
    # CSV로 저장
    path_df.to_csv('home_to_cafe.csv', index=False)
    print(f'경로가 home_to_cafe.csv 파일로 저장되었습니다. (총 {len(path)}단계)')
    print('저장된 경로:')
    print(path_df.head(10))
    if len(path) > 10:
        print('...')
        print(path_df.tail(3))


def main():
    """
    메인 실행 함수
    """
    print('반달곰 커피 최단경로 찾기 프로젝트 - 3단계')
    print('=' * 50)
    
    # 데이터 불러오기
    data, category_df = load_processed_data()
    print(f'불러온 데이터 크기: {data.shape}')
    print()
    
    # 시작점과 끝점 찾기
    start_point, end_point = find_start_and_end_points(data, category_df)
    
    if start_point is None or end_point is None:
        print('시작점 또는 끝점을 찾을 수 없어서 경로 탐색을 중단합니다.')
        return
    
    print()
    
    # 격자 지도 생성
    grid_map = create_grid_map(data, start_point)
    print(f'격자 지도 생성 완료: {len(grid_map)}개 셀')
    
    # 장애물 통계
    obstacles = sum(1 for v in grid_map.values() if v == 'obstacle')
    print(f'장애물 개수: {obstacles}개')
    print()
    
    # BFS로 최단경로 찾기
    print('=== BFS 최단경로 탐색 시작 ===')
    shortest_path = bfs_shortest_path(grid_map, start_point, end_point)
    
    if shortest_path:
        print('경로 탐색 성공!')
        print(f'최단 거리: {len(shortest_path) - 1}칸')
        print()
        
        # 경로 시각화
        visualize_path(data, category_df, shortest_path, start_point, end_point)
        
        # 경로 CSV로 저장
        save_path_to_csv(shortest_path)
    else:
        print('경로를 찾을 수 없습니다.')
    
    print('3단계 최단경로 탐색 완료!')


if __name__ == '__main__':
    main()