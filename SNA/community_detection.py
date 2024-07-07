import pandas as pd
import community.community_louvain as cl
import matplotlib.cm as cm
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


def detect_communities(G_data, resolution=1.08, random_state=42):
    """
    Community detection을 수행하는 함수

    Parameters:
    - G_data (Graph): 입력 네트워크 그래프
    - resolution (float): Community resolution
    - random_state (int): 랜덤 시드 값

    Returns:
    - dict: 노드별 커뮤니티 ID
    """
    return cl.best_partition(G_data, random_state=random_state, resolution=resolution)


def visualize_communities(G_data, partition):
    """
    커뮤니티를 시각화하는 함수

    Parameters:
    - G_data (Graph): 입력 네트워크 그래프
    - partition (dict): 노드별 커뮤니티 ID
    """
    pos = nx.spring_layout(G_data)
    degree = nx.degree(G_data)

    plt.figure(figsize=(40, 40))
    cmap = cm.get_cmap('Blues', max(partition.values()) + 1)
    nx.draw_networkx_nodes(G_data, pos, partition.keys(), node_size=[10 + v[1] * 10 for v in degree],
                           cmap=cmap, node_color=list(partition.values()))
    nx.draw_networkx_edges(G_data, pos, alpha=0.5, width=0.15)
    nx.draw_networkx_labels(G_data, pos, font_size=12, font_family='Malgun Gothic')

    plt.show()


def get_cluster_info(G_data, partition):
    """
    클러스터 정보를 얻는 함수

    Parameters:
    - G_data (Graph): 입력 네트워크 그래프
    - partition (dict): 노드별 커뮤니티 ID

    Returns:
    - DataFrame: 클러스터별 노드 정보
    - list: 클러스터별 노드 리스트
    """
    num_clusters = len(set(partition.values()))
    node_degrees = sorted(G_data.degree, key=lambda x: x[1], reverse=True)

    sorted_node = [node for node, degree in node_degrees]
    cluster_idlist = [partition[node] for node in sorted_node]

    sorted_df = pd.DataFrame({"Label": sorted_node, "cluster_num": cluster_idlist})

    cluster_lists = [[] for _ in range(num_clusters)]
    for i in range(num_clusters):
        cluster_lists[i] = list(sorted_df[sorted_df["cluster_num"] == i]["Label"])

    return sorted_df, cluster_lists


def main():
    # 데이터 불러오기
    df = load_sna_data('SNA_df.csv')

    # 그래프 생성
    G_data = create_graph(df)

    # 커뮤니티 탐지
    partition = detect_communities(G_data)

    # 커뮤니티 시각화
    visualize_communities(G_data, partition)

    # 클러스터 정보 얻기
    sorted_df, cluster_lists = get_cluster_info(G_data, partition)

    # 클러스터별 단어 출력
    num_clusters = len(cluster_lists)
    for i in range(num_clusters):
        print(f"Cluster {i} ({len(cluster_lists[i])} nodes): {cluster_lists[i][:10]}")


if __name__ == "__main__":
    main()