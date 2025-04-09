# ZeoAnalyzer

## 概述

ZeoAnalyzer是一个模块化的沸石分析框架，其主要任务是通过调用zeo++对cif文件进行分析，提取特征，聚类、降维分析并可视化展示。
ZeoAnalyzer由四个可自定义的子模块和一个自带的show方法组成，如下所示：
```
ZeoAnalyzer - show
 | - FeatureExtractor
 | - FeatureVectorGenerator
 | - FeatureClusterer
 | - FeatureDimReducer
```

接下来，我将根据顺序依次介绍每个子模块（接口）。

### FeatureExtractor

该接口定义了调用zeo++对cif文件进行分析并提取特征的过程。

接口由两个方法组成，`zeopp_command_generator`和`zeopp_file_analyzer`，分别对应了调用zeo++对cif进行分析与从zeo++的输出文件读取内容的操作。

#### zeopp_command_generator

`zeopp_command_generator`传入cif文件名`cif_file`与输出文件名基底`output_file_base`（输出文件名的后缀待添加，如果使用`-res`分析方法，则输出文件名为`output_file_base.res`，以此类推）。该方法输出一个str类型的命令`command`，用于执行zeo++。

#### zeopp_file_analyzer

`zeopp_file_analyzer`传入输出文件名基底`output_file_base`，输出一个dict类型的特征字典`feature_dict`，字典的key为特征名称，value为特征值。

#### 代码定义

```python
class FeatureExtractor:
    def __init__(self, zeopp_command_generator, zeopp_file_analyzer):
        self.zeopp_command_generator = zeopp_command_generator
        self.zeopp_file_analyzer = zeopp_file_analyzer

    def generate_zeopp_command(self, cif_file, output_file_base):
        return self.zeopp_command_generator(cif_file, output_file_base)

    def analyse_zeopp_file(self, output_file_base):
        return self.zeopp_file_analyzer(output_file_base)

    def extract_features(self, cif_file, output_file_base):
        command = self.generate_zeopp_command(cif_file, output_file_base)
        self.zeopp_execute_command(command)

    @staticmethod
    def zeopp_execute_command(command):
        subprocess.run(command, stdout=subprocess.DEVNULL, shell=True, check=True)
```

#### 自定义分析与读取结果的过程

通过自定义`zeopp_command_generator`和`zeopp_file_analyzer`方法，可以模块化地为ZeoAnalyzer添加调用zeo++进行分析与读取结果的过程。

案例：定义`-res`分析方法的调用与结果读取

```python
# 定义调用zeo++进行分析的指令
def zeopp_res_command_generator(cif_file, output_file_base):
    return f"./network -res {output_file_base}.res {cif_file}"

# 定义从输出读取分析结果的方式
def zeopp_res_file_analyzer(output_file_base):
    assert os.path.exists(output_file_base + '.res'), f"{output_file_base}.res doesn't exist!"

    with open(output_file_base + '.res', 'r') as f:
        output_text = f.read()

    feature_dict = {}
    outputs = output_text.split()
    feature_dict['maxIncDiam'] = float(outputs[1])
    feature_dict['maxDiam'] = float(outputs[2])
    feature_dict['incDiam'] = float(outputs[3])

    return feature_dict

# 组合为一个FeatureExtractor对象
zeopp_res = FeatureExtractor(zeopp_res_command_generator, zeopp_res_file_analyzer)
```
除此之外，目前项目中还实现了`-sa`和`-vol`分析方法的调用与结果的解析，详见`feature_extractor.py`。

本项目的所有“接口-定义”逻辑均按照这种方式实现，后续不再赘述。

### FeatureVectorGenerator

该接口定义了将多个`feature_dict`组成的列表`feature_dict_list`特征化为一个1d-numpy数组`feature_vector`的过程。

该接口包含一个方法`dict_list_to_vector`。

#### dict_list_to_vector

`dict_list_to_vector`输入一个由多个`feature_dict`组成的列表`feature_dict_list`，输出一个1d-numpy数组`feature_vector`。


#### 代码定义

```python
class FeatureVectorGenerator:
    def __init__(self, dict_list_to_vector):
        self.dict_list_to_vectors = dict_list_to_vector

    def generate_feature_vectors(self, feature_dict_list):
        return self.dict_list_to_vectors(feature_dict_list)
```

#### 自定义特征化过程

通过自定义`dict_list_to_vector`方法传入构造函数创建FeatureVectorGenerator的方式自定义特征化过程。

目前仅实现了将所有特征暴力拼接的方法，见`feature_vector_generator.py`。

### FeatureClusterer

该接口包含一个方法`clustering_algorithm`，定义了聚类分析过程。该接口还包含一个属性`algorithm_name`,用于储存聚类方法的名称。

#### clustering_algorithm

`clustering_algorithm`的输入为由n个特征向量`feature_vector`组成的nd-numpy数组`feature_vectors`，输出为1d-numpy数组`cluster_labels`，表示聚类标签。

#### 代码定义

```python
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
```

#### 自定义聚类方法

通过自定义`clustering_algorithm`方法并传入构造函数FeatureClusterer的方式自定义聚类方法。

目前定义了两种聚类方法`K-Means`和`DBSCAN`，详见`feature_clusterer.py`。

### FeatureDimReducer

该接口包含一个方法`reduction_algorithm`，定义了降维分析过程。该接口还包含一个属性`algorithm_name`，用于储存降维方法的名称。

#### reduction_algorithm

`reduction_algorithm`的输入为由n个特征向量`feature_vector`组成的nd-numpy数组`feature_vectors`，输出为`2d-numpy`数组`feature_vectors_reduced`。

#### 代码定义

```python
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
```

#### 自定义降维过程

通过自定义`reduction_algorithm`方法并传入构造函数FeatureDimReducer的方式自定义降维方法。

目前定义了三种降维方法，分别是`t-SNE`、`UMAP`和`PCA`，详见`feature_dim_reducer.py`。

### ZeoAnalyzer.show

该方法定义了可视化过程。可输入参数分别为列表`selected_cif_file_list`，定义了需要被展示的cif文件组，与`img_save`，定义了图片输出路径。如果`selected_cif_file_list`为None，则默认展示所有cif文件的分析结果；如果`img_save`为None，则默认调用`plt.show()`展示图片并不保存至本地。

## 使用

`main.py`是项目的主入口。

```python
if __name__ == "__main__":
    # 定义zeo++使用的分析方法
    feature_extractors = [zeopp_res, zeopp_sa, zeopp_vol]
    
    # 创建ZeoAnalyzer对象，传入分析方法、特征化方法、聚类方法与降维方法
    analyzer = ZeoAnalyzer(
        feature_extractors=feature_extractors,
        feature_vector_generator=feature_concatenator,
        feature_clusterer=k_means_clusterer,
        feature_dim_reducer=pca_reducer,
        output_dir="./demo_output_1000" # 调用zeo++时分析文件的输出目录
    )
    
    # 定义cif文件的目录
    cif_dir = "../../database/demo_dataset_1000"
    # 可以使用列表的形式传入多个目录
    # cif_dir = ['dir1', 'dir2', ...]
    
    # 调用zeo++对cif文件进行分析
    analyzer.analyse_cifs(cif_dir)
    # 如果已经调用过zeo++生成分析结果，只需要将沸石的特征从对应文件中提取出来
    # 就将传入的参数zeopp_already_invoked设置为True
    # analyzer.analyse_cifs(cif_dir, zeopp_already_invoked=True)
    
    # 对特征进行聚类、降维和可视化
    analyzer.cluster_reduce_show()
    # 如果需要将可视化结果保存至本地，可以传入img_save参数
    # analyzer.cluster_reduce_show(img_save="images/pca_dbscan.png")
    # 如果需要对特定部分对cif_file进行可视化，可以传入selected_cif_file_list参数
    # analyzer.cluster_reduce_show(selected_cif_file_list=...)
    # 聚类、降维、可视化三步可以分布进行
    # analyzer.cluster_feature_vectors(selected_cif_files)
    # analyzer.reduce_feature_vectors(selected_cif_files)
    # analyzer.show(selected_cif_files, img_save)
```