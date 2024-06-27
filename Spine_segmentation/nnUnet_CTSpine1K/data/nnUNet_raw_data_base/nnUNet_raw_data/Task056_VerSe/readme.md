## 本文件内容：
1. 保存了nnunet的分割结果、原始图像、label
2. 涉及第二步分割以及量化计算的所有脚本文件
3. 涉及标准人数据、第一阶段数据集、第二阶段数据集

## 相关文件
1. metrics.py:用于miou计算的util脚本
2. result_G0PA0:标准人的原图、label、nnunet分割以及分割结果

    ```
    1. `img_o` 原图
    2. `label` 手工标注的标签，此处为柱体分割(nnunet)结果生成的，因为论文中不需要标准人的手动标注的标签，院方也没有提供。
    3. `seg` nnunet分割结果
    4. `seg_mask` nnunet分割结果转换为的0-1掩膜,用于量化检测阶段使用
    5. `out_ct_begin_27_-1_20231228_2` 皮质松质分割结果
        5.1 *_y.nii y视角下分割结果
        5.2 *_z.nii z视角下分割结果
        5.3 *_all_cancellous.nii 双视角融合的松质分割结果
        5.4 *_all_corte.nii 双视角融合的皮质分割结果
    6. `label_seg`将label中需要的脊柱节转化为01mask
    7. `out_ct_begin_27_-1_20220204_ablation_2` 消融实验时使用的保存位置

    ```
3. result_november：第一批数据结果
4. result_stage2：第二批数据结果

5. imagesTr、imagesTs、labelsTr:nnunet分割相关的文件夹


7. z_calculate_stage1_2_para_ct_27_-1_all：额外保存了阈值分割，stage1 2都有----------作为当前主线最新进展,输出结果放在“out_ct_begin_27_-1_20231228_2”，其文件作用如下：
```
1. seg.py  分割皮质、松质、yz视角
2. seg_to_mask.py 获得nnunet分割结果中所需的脊柱节，转换为01mask
3. label_2_mask.py 获得label中所需的脊柱节，转换为01mask
4. select_all_193_2.py:皮质/松质密度计算，误差统计。输出xlsx文件以及npy文件,论文实验的.npy文件数据保存在硬盘`YangGuoqing/spine/result/npy/`中。

5. draw.py 使用npy文件的数据统计绘图
6. get_miou.py  输出分割的miou
7. CT: 量化检测四节脊柱节松质骨质流失比例，四节平均值以及骨质疏松程度分类
8. CT2: 对比实验，比较机器学习方法，gth，人工切片三种方法在三节脊柱平均的密度、流失比例以及诊断归类。输出xlsx  `result_cancellous_with_mean_3.xlsx`
```


9. `z_calculate_stage1_2_para_ct_27_-1_all_Ablation`做消融实验使用的代码副本，保存在硬盘`YangGuoqing/spine/ablation_study/code/`中
