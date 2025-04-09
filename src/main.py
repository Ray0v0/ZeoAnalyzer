from feature_extractor import *
from zeo_analyzer import ZeoAnalyzer

if __name__ == '__main__':
    feature_extractors = [zeopp_res, zeopp_sa, zeopp_vol]
    analyzer = ZeoAnalyzer(
        feature_extractors=feature_extractors,
        output_dir="./demo_output_1000"
    )
    cif_dir = "../database/demo_dataset_1000"
    analyzer.analyse_cifs(cif_dir, zeopp_already_invoked=True)

