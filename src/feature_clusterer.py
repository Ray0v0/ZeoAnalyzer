import numpy as np
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler


class FeatureClusterer:
    def __init__(self, clustering_algorithm, algorithm_name):
        self.clustering_algorithm = clustering_algorithm
        self.algorithm_name = algorithm_name

    def cluster(self, feature_vector_dict, cif_files):
        selected_feature_vector_list = []
        for cif_file in cif_files:
            selected_feature_vector_list.append(feature_vector_dict[cif_file])

        # 标准化
        feature_vectors = np.vstack(selected_feature_vector_list)
        scaler = StandardScaler()
        feature_vectors_scaled = scaler.fit_transform(feature_vectors)

        # 聚类
        cluster_labels = self.clustering_algorithm(feature_vectors_scaled)
        return cluster_labels

# 定义k-means聚类器

def k_means(feature_vectors, n_clusters=5):
    kmeans = KMeans(n_clusters=n_clusters, n_init='auto', random_state=42)
    cluster_labels = kmeans.fit_predict(feature_vectors)
    return cluster_labels

k_means_clusterer = FeatureClusterer(k_means, "K-Means")

# 定义dbscan聚类器

def dbscan(feature_vectors, eps=0.5, min_samples=5):
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    cluster_labels = dbscan.fit_predict(feature_vectors)
    return cluster_labels

dbscan_clusterer = FeatureClusterer(dbscan, "DBSCAN")