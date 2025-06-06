from feature_extractor import *
from feature_vector_generator import *
from feature_clusterer import *
from feature_dim_reducer import *
from zeo_analyzer import ZeoAnalyzer

if __name__ == '__main__':
    feature_extractors = [zeopp_res, zeopp_sa, zeopp_vol]
    analyzer = ZeoAnalyzer(
        feature_extractors=feature_extractors,
        feature_vector_generator=feature_concatenator,
        feature_clusterer=k_means_clusterer,
        feature_dim_reducer=pca_reducer,
        output_dir="./demo_output_1000"
    )
    cif_dir = "../../database/demo_dataset_1000"
    analyzer.analyse_cifs(cif_dir, zeopp_already_invoked=True)
    analyzer.cluster_reduce_show(img_save="images/pca_dbscan.png")
