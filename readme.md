# 骨密度项目代码：

项目时间 2022.5.21
内容：胸腔脊柱分割，量化计算脊柱密度

## 文件

1. `Dicom2niigz.py`:将Dicom格式的原始数据转换为nii.zg格式

2. `dataset`：保存原始Dicom数据，以及生成的nii.gz数据

    2.1 `dataset/GO`:存放原始Dicom数据，示例：PA0
    
    2.2 `dataset/G0_middataset`:中间临时数据保存地点
    
    2.3 `dataset/G0_result`: 格式转换结果，示例：PA0_0000.nii.gz

3. `Spine_segmentation`: 脊柱分割、松质分割、量化检测等相关。使用CTSpine1K数据集建议的nnUnet 进行分割，在CTSpine1K 数据集上训练分割，然后用在重医的数据集上

    3.1 `Spine_segmentation/nnUnet_CTSpine1K/CTSpine1K_code/CTSpine1K` 使用nnunet进行脊柱柱体等分割

    3.2 `Spine_segmentation/nnUnet_CTSpine1K/data`: 柱体分割结果保存；进行松质分割，量化检测等。   

        3.2.1 `data/nnUNet_trained_models` nnunet模型参数

        3.2.2 `data/nnUNet_raw_data_base` 柱体分割结果保存；进行松质分割，量化检测等。详见"nnUNet_raw_data_base"部分

4. `Spine/Spine_segmentation/nnUnet_CTSpine1K/data/nnUNet_raw_data_base`





## 运行示例：

### 一、 环境以及模型配置

1. 创建环境
```shell
conda create -n new_environment_name --file requirement.txt
```
2. 
```
conda activate new_environment_name
```

3. 将`Spine/nnunet`复制到环境中。在 Conda 环境中，通常包安装在` <conda_env_path>/lib/pythonX.X/site-packages/` 目录下，其中 `<conda_env_path> `是你的 Conda 环境的路径，X.X 是 Python 的版本号。

4. 模型下载：在硬盘中下载，并将`nnUNet_trained_models`文件夹放在`Spine/Spine_segmentation/nnUnet_CTSpine1K/data/`

5. 其他环境配置 
打开`~/.bashrc`
``` 
vim ~/.bashrc
```
添加如下代码
```
export nnUNet_raw_data_base="<your_path>/nnUNet_raw_data_base"
export nnUNet_preprocessed="<your_path>/nnUNet_preprocessed"
export RESULTS_FOLDER="<your_path>/nnUNet_trained_models"
```

备注：实验时使用的环境压缩包保存在硬盘`YangGuoqing/spine/env/`

### 二、上传数据以及格式转换
    1. 上传Dicom数据如“PA0”到“Spine/dataset/G0/”下
    2. 修改“Dicom2niigz.py”相关路径
    3. 运行“Dicom2niigz.py”
    4. 在“Spine/dataset/G0_result/”获得转换后到结果


### 三、脊柱柱体分割

#### 1. 单个CT病例单分割：

1. 将nii.gz格式数据如“PA0_0000.nii.gz”保存在`Spine/Spine_segmentation/nnUnet_CTSpine1K/data/nnUNet_raw_data_base/nnUNet_raw_data/Task056_VerSe/imagesTs/`。

2. 确保`Spine/Spine_segmentation/nnUnet_CTSpine1K/data/nnUNet_raw_data_base/nnUNet_raw_data/Task056_VerSe/`下存在名为`predict`的文件夹。

3. 
```
cd Spine/Spine_segmentation/nnUnet_CTSpine1K/CTSpine1K_code/CTSpine1K
```

4. 
```
nohup bash test.sh > test.out&
```

5. 推理结束后在`Spine/Spine_segmentation/nnUnet_CTSpine1K/data/nnUNet_raw_data_base/nnUNet_raw_data/Task056_VerSe/predict/`获得结果。

注意：

1. 推理时间较长，因此建议使用nohup 的形式在后台处理

2. 推理过程占用大约2G多的GPU显存资源，但是占用大量的内存资源。并且如果内存资源用尽的话进程会被kill掉，nnunet作者在github中解释说他们不擅长多线程编程，因此可能有内存泄露等情况。所以为了程序顺利运行，本项目在实验室容器平台上申请了192GB等内存空间，并且限制线程数量为1（设置方法后面介绍）

#### 2. 批处理
1. 保证在`Spine/dadaset/`下的nii.gz原始数据有类似如下结构：
```
        Spine/
            dataset/
                G2_result/
                    PA1_0000.nii.gz
                    PA2_0000.nii.gz
                    PA3_0000.nii.gz
                    ······
```
2. 
```
cd Spine/Spine_segmentation/nnUnet_CTSpine1K/CTSpine1K_code/CTSpine1K
```
3. 参考`test_G2.sh`的内容进行修改
4. 
```
nohup bash test_G2.sh > test_G2.out&
```
5. 在`Spine/Spine_segmentation/nnUnet_CTSpine1K/data/nnUNet_raw_data_base/nnUNet_raw_data/Task056_VerSe/` 获得对应结果


四、松质分割

1.
```shell
cd Spine/Spine_segmentation/nnUnet_CTSpine1K/data/nnUNet_raw_data_base/nnUNet_raw_data/Task056_VerSe
```
2. 数据准备。以分割第二批数据为例，确保文件夹result_stage2下有如下结构：
```
result_stage2:
    /img_o                   原图
        /imagesTs_G1_PA1   
            /PA1_0000.nii.gz
        /imagesTs_G1_PA2
            /PA2_0000.nii.gz
        ...
    /seg                   脊柱柱体分割结果  
        /predict_G1_PA1
            /PA1.nii.gz
        /predict_G1_PA2
            /PA2.nii.gz
        ...
```
或者从硬盘`YangGuoqing/spine/result/seg_result`,并将`result_G0PA0`,`result_november`,`result_stage2`文件夹放到`Spine/Spine_segmentation/nnUnet_CTSpine1K/data/nnUNet_raw_data_base/nnUNet_raw_data/Task056_VerSe/`
3. 
```shell
cd z_calculate_stage1_2_para_ct_27_-1_all
```

4. 按照需要修改`seg.py`,`select_all_193_2.py`,`draw.py`以及`get_miou.py`中的路径
5.
```shell
nohup bash main.sh > main.out&
```
6. 在`out_ct_begin_27_-1_20231228_2`文件夹中获得皮质和松质分割结果。


五、量化检测

(一) 量化检测四节脊柱节松质骨质流失比例，四节平均值以及骨质疏松程度分类
1. 
```shell
cd Spine/Spine_segmentation/nnUnet_CTSpine1K/data/nnUNet_raw_data_base/nnUNet_raw_data/Task056_VerSe/z_calculate_stage1_2_para_ct_27_-1_all/CT
```
2. 
```shell
nohup bash ct.sh > ct.out&
```
论文中的实验结果查看 硬盘中`YangGuoqing/spine/result/CT/`

（二）对比实验：比较机器学习方法，gth，人工切片三种方法在三节脊柱平均的密度、流失比例以及诊断归类。输出xlsx  `result_cancellous_with_mean_3.xlsx`

1. 
```shell
cd Spine/Spine_segmentation/nnUnet_CTSpine1K/data/nnUNet_raw_data_base/nnUNet_raw_data/Task056_VerSe/z_calculate_stage1_2_para_ct_27_-1_all/CT_2
```
2. 
```shell
nohup bash ct.sh > ct.out&
```
论文中的实验结果查看 硬盘中`YangGuoqing/spine/result/CT_2/`



