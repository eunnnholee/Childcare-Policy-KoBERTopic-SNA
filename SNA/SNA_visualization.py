import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


def load_sna_data(file_path):
    """
    CSV 파일을 불러오는 함수

    Parameters:
    - file_path (str): 불러올 CSV 파일의 경로

    Returns:
    - DataFrame: 불러온 데이터프레임
    """
    return pd.read_csv(file_path, encoding='cp949', index_col=0)


def create_graph(df):
    """
    데이터프레임에서 그래프를 생성하는 함수

    Parameters:
    - df (DataFrame): 입력 데이터프레임

    Returns:
    - Graph: 생성된 네트워크 그래프
    """
    return nx.from_pandas_edgelist(df, source='Source', target='Target', edge_attr='Weight')


def visualize_graph(G_data):
    """
    그래프를 시각화하는 함수

    Parameters:
    - G_data (Graph): 입력 네트워크 그래프
    """
    plt.rc('font', family='Malgun Gothic')
    plt.figure(figsize=(40, 40))

    degree = nx.degree(G_data)
    pos = nx.spring_layout(G_data)

    nx.draw(G_data, pos, with_labels=True, node_size=[10 + v[1] * 10 for v in degree], font_size=15, width=0.05,
            font_family='Malgun Gothic')
    edge_weight = nx.get_edge_attributes(G_data, 'Weight')
    nx.draw_networkx_edge_labels(G_data, pos, edge_labels=edge_weight, alpha=0.3, font_size=3,
                                 font_family='Malgun Gothic')

    plt.show()


def graph_statistics(G_data):
    """
    그래프의 통계치를 계산하는 함수

    Parameters:
    - G_data (Graph): 입력 네트워크 그래프

    Returns:
    - dict: 그래프 통계치
    """
    stats = {
        'Number of nodes': nx.number_of_nodes(G_data),
        'Number of edges': nx.number_of_edges(G_data),
        'Diameter': nx.diameter(G_data),
        'Density': nx.density(G_data),
        'Transitivity': nx.transitivity(G_data),
        'Reciprocity': nx.reciprocity(G_data)
    }
    return stats


def centrality_measures(G_data):
    """
    중심성 측정을 수행하는 함수

    Parameters:
    - G_data (Graph): 입력 네트워크 그래프

    Returns:
    - dict: 중심성 측정 결과
    """
    deg_cen = nx.degree_centrality(G_data)
    bet_cen = nx.betweenness_centrality(G_data)
    clo_cen = nx.closeness_centrality(G_data)
    eig_cen = nx.eigenvector_centrality(G_data)

    centrality = {
        'Degree Centrality': sorted(deg_cen.items(), key=lambda x: x[1], reverse=True)[:3],
        'Betweenness Centrality': sorted(bet_cen.items(), key=lambda x: x[1], reverse=True)[:3],
        'Closeness Centrality': sorted(clo_cen.items(), key=lambda x: x[1], reverse=True)[:3],
        'Eigenvector Centrality': sorted(eig_cen.items(), key=lambda x: x[1], reverse=True)[:3]
    }
    return centrality


def main():
    # 데이터 불러오기
    df = load_sna_data('SNA_df.csv')

    # 그래프 생성
    G_data = create_graph(df)

    # 그래프 시각화
    visualize_graph(G_data)

    # 그래프 통계 출력
    stats = graph_statistics(G_data)
    for key, value in stats.items():
        print(f'{key}: {value}')

    # 중심성 측정 결과 출력
    centrality = centrality_measures(G_data)
    for key, value in centrality.items():
        print(f'{key}:\n', value)


if __name__ == "__main__":
    main()