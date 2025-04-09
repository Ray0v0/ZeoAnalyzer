import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
import umap


class FeatureDimReducer:
    def __init__(self, reduction_algorithm, algorithm_name):
        self.reduction_algorithm = reduction_algorithm
        self.algorithm_name = algorithm_name

    def reduce(self, feature_vector_dict, cif_files):
        selected_feature_vector_list = []
        for cif_file in cif_files:
            selected_feature_vector_list.append(feature_vector_dict[cif_file])

        # 标准化
        feature_vectors = np.vstack(selected_feature_vector_list)
        scaler = StandardScaler()
        feature_vectors_scaled = scaler.fit_transform(feature_vectors)

        # 降维
        feature_vectors_reduced = self.reduction_algorithm(feature_vectors_scaled)
        return feature_vectors_reduced

# 定义t-sne降维器

def t_sne(feature_vectors):
    t_sne = TSNE(n_components=2, random_state=42)
    feature_vectors_tsne = t_sne.fit_transform(feature_vectors)
    return feature_vectors_tsne

t_sne_reducer = FeatureDimReducer(t_sne, "t-SNE")

# 定义umap降维器

def umap_algo(feature_vectors):
    umap_algo = umap.UMAP()
    feature_vectors_umap = umap_algo.fit_transform(feature_vectors)
    return feature_vectors_umap

umap_reducer = FeatureDimReducer(umap_algo, "UMAP")

# 定义pca降维器

def pca(feature_vectors):
    pca = PCA(n_components=2)
    feature_vectors_pca = pca.fit_transform(feature_vectors)
    return feature_vectors_pca

pca_reducer = FeatureDimReducer(pca, "PCA")