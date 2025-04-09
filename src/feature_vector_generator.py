import numpy as np

class FeatureVectorGenerator:
    def __init__(self, dict_list_to_vector):
        self.dict_list_to_vector = dict_list_to_vector

    def generate_feature_vector(self, feature_dict_list):
        return self.dict_list_to_vector(feature_dict_list)

# 定义 feature_concatenator

def concatenate_all_features(feature_dict_list):
    feature_vector_list = []
    for feature_dict in feature_dict_list:
        for _, value in feature_dict.items():
            feature_vector_list.append(value)
    return np.array(feature_vector_list)

feature_concatenator = FeatureVectorGenerator(concatenate_all_features)