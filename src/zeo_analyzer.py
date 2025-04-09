import os
from concurrent.futures import ThreadPoolExecutor

from tqdm import tqdm


class ZeoAnalyzer:
    def __init__(self, feature_extractors, feature_vector_generator, feature_clusterer, feature_dim_reducer, output_dir="../output/"):
        self.feature_extractors = feature_extractors
        self.feature_vector_generator = feature_vector_generator
        self.feature_clusterer = feature_clusterer
        self.feature_dim_reducer = feature_dim_reducer
        self.output_dir = output_dir
        self.feature_vector_dict = {}
        self.zeopp_already_invoked = False
        self.command_output = True
        self.cif_file_list = None
        self.cluster_label_dict = {}
        self.reduced_feature_vector_dict = {}

    def analyse_cifs(self, cif_dirs, zeopp_already_invoked=False):
        if self.command_output:
            print("Analysing cifs...")

        self.zeopp_already_invoked = zeopp_already_invoked

        # 支持输入为单个文件夹路径或多个文件夹路径列表
        if type(cif_dirs) == str:
            cif_dirs = [cif_dirs]

        # 确保输入的路径都存在
        for cif_dir in cif_dirs:
            assert os.path.exists(cif_dir), f"Directory {cif_dir} doesn't exist!"

        # 提取输入路径中的cif文件
        self.cif_file_list = []
        for cif_dir in cif_dirs:
            for file in os.listdir(cif_dir):
                if file.endswith(".cif"):
                    self.cif_file_list.append(os.path.join(cif_dir, file))

        # 确保输入的路径中存在cif文件
        assert len(self.cif_file_list) != 0, f"No cif files found in Directory {cif_dirs}!"

        # 并行化分析cif文件
        with ThreadPoolExecutor() as executor:
            list(tqdm(executor.map(self.analyse_cif, self.cif_file_list), total=len(self.cif_file_list)))

    def analyse_cif(self, cif_file):
        # 确认cif文件和输出目录存在
        assert(os.path.exists(cif_file)), f"{cif_file} does not exist!"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # 调用zeopp分析cif文件
        output_file_base = os.path.join(self.output_dir, os.path.splitext(os.path.basename(cif_file))[0])
        feature_dict_list = []
        for feature_extractor in self.feature_extractors:
            if not self.zeopp_already_invoked:
                feature_extractor.extract_features(cif_file, output_file_base)
            feature_dict_list.append(feature_extractor.analyse_zeopp_file(output_file_base))

        # 向量化并存入以文件名为索引的字典中
        feature_vector = self.feature_vector_generator.generate_feature_vectors(feature_dict_list)
        self.feature_vector_dict[cif_file] = feature_vector

    def cluster_feature_vectors(self, selected_cif_files=None):
        if self.command_output:
            print("Clustering feature vectors...")

        if selected_cif_files is None:
            selected_cif_files = self.cif_file_list

        # 聚类并储存为文件名为索引的字典
        cluster_labels = self.feature_clusterer.cluster(self.feature_vector_dict, selected_cif_files)
        for i in range(len(selected_cif_files)):
            self.cluster_label_dict[selected_cif_files[i]] = cluster_labels[i]

    def reduce_feature_vectors(self, selected_cif_files=None):
        if self.command_output:
            print("Reducing feature vectors...")

        if selected_cif_files is None:
            selected_cif_files = self.cif_file_list

        # 降维并储存为文件名为索引的字典
        reduced_feature_vectors = self.feature_dim_reducer.reduce(self.feature_vector_dict, selected_cif_files)
        for i in range(len(selected_cif_files)):
            self.reduced_feature_vector_dict[selected_cif_files[i]] = reduced_feature_vectors[i]

