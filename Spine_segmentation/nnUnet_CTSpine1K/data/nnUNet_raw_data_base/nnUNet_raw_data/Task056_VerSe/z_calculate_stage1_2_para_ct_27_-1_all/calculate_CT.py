####计算CT值
#
#整图平均CT，分段皮质、松质、皮质+松质平均
####
import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from collections import Counter
import cv2
from PIL import Image
import SimpleITK as sitk


file_list = ["result_november","result_stage2"]

for file_list_n in file_list:

    spine_seg_root = "/root/Spine/Spine/Spine_segmentation/nnUnet_CTSpine1K/data/nnUNet_raw_data_base/nnUNet_raw_data/Task056_VerSe/{}/seg".format(file_list_n)
    cortex_seg_root = "/root/Spine/Spine/Spine_segmentation/nnUnet_CTSpine1K/data/nnUNet_raw_data_base/nnUNet_raw_data/Task056_VerSe/{}/out".format(file_list_n)
    img_or_root = "/root/Spine/Spine/Spine_segmentation/nnUnet_CTSpine1K/data/nnUNet_raw_data_base/nnUNet_raw_data/Task056_VerSe/{}/img_o".format(file_list_n)
    label_root = "/root/Spine/Spine/Spine_segmentation/nnUnet_CTSpine1K/data/nnUNet_raw_data_base/nnUNet_raw_data/Task056_VerSe/{}/label".format(file_list_n)
    seg_pred_file_root = os.listdir(spine_seg_root)
    global_percentage_all = []
    global_percentage_cortex = []
    global_percentage_Cancellous = []
    for file in seg_pred_file_root:
        ##############
        Gn = file.split("_")[1]
        PAn = file.split("_")[2]
        spine_seg_pth = os.path.join(spine_seg_root,file,PAn+".nii.gz")
        
        label_pth = os.path.join(label_root,Gn,PAn+".nii.gz")

        img_or_path = os.path.join(img_or_root,"imagesTs_"+Gn+"_"+PAn,PAn+"_0000.nii.gz")

        cortex_seg_path = os.path.join(cortex_seg_root,file,"{}{}_K11C0k4i5".format(Gn,PAn),"PA_k4i4_3_all.nii.gz")
        print("processing "+Gn+" "+PAn)
        
        ##############end

        # name = file.split("_")[-1]
        # len_name = len(name);
        # data_file = file[0:-1*len_name-1]
        # spine_seg_pth = os.path.join(spine_seg_root,file,name+".nii.gz")
        # label_pth = os.path.join(label_root,data_file,data_file+"_"+name+"_label.nii.gz")

        # img_or_path = os.path.join(img_or_root,"imagesTs"+data_file[7:]+"_"+name,name+"_0000.nii.gz")
        # cortex_seg_path = os.path.join(cortex_seg_root,file,"K11C0k4i5","PA_k4i4_3_all.nii.gz")
        # print("processing "+data_file+" "+name)

    #数据读取模块
    ### 脊柱
    # spine_seg_pth = "/root/Spine/Spine/Spine_segmentation/nnUnet_CTSpine1K/data/nnUNet_raw_data_base/nnUNet_raw_data/Task056_VerSe/result_november/seg/predict_after_november/predict_10_13__11_7_PA0/PA0.nii.gz"
        # print(spine_seg_pth)
        spine_seg = sitk.ReadImage(spine_seg_pth)
        origin =spine_seg.GetOrigin()
        direction = spine_seg.GetDirection()
        space = spine_seg.GetSpacing()
        spine_seg = sitk.GetArrayFromImage(spine_seg)
    #################
    #添加策略
        spine_seg[spine_seg>21.5] = 0
        spine_seg[spine_seg<17.5] = 0
        spine_seg[spine_seg<0] = 0
    #################

        slice_num = spine_seg.shape[0]
    ### 皮质cortex
        # cortex_seg_path =  "/root/Spine/Spine/Spine_segmentation/nnUnet_CTSpine1K/data/nnUNet_raw_data_base/nnUNet_raw_data/Task056_VerSe/result_november/out/predict_10_13__11_7_PA0/K11C0k4i5/PA_k4i4_3_all.nii.gz"
        cortex_seg = sitk.ReadImage(cortex_seg_path)
        cortex_seg = sitk.GetArrayFromImage(cortex_seg)

    ###松Cancellous
    ### 原图
    # img_or_path =  "/root/Spine/Spine/Spine_segmentation/nnUnet_CTSpine1K/data/nnUNet_raw_data_base/nnUNet_raw_data/Task056_VerSe/imagesTs_10_13__11_7_PA0/PA0_0000.nii.gz"
        img_or = sitk.ReadImage(img_or_path)
        img_or = sitk.GetArrayFromImage(img_or)

    ### gth
    # label_pth = "/root/Spine/Spine/Spine_segmentation/nnUnet_CTSpine1K/data/nnUNet_raw_data_base/nnUNet_raw_data/Task056_VerSe/result_november/label/predict_10_13__11_7/predict_10_13__11_7_PA0_label.nii.gz"
        label = sitk.ReadImage(label_pth)
        label = sitk.GetArrayFromImage(label)

    #######################################
    ### 计算整个平均CT
        saved_pth_img_seg = "calculate_CT"
        if not os.path.exists(saved_pth_img_seg):
            os.makedirs(saved_pth_img_seg) 

        spine_mask = spine_seg.astype(bool).astype(np.int16)
        img_seg = img_or*spine_mask
        counter_nonezeros = np.count_nonzero(img_seg)
        ave_CT_all = img_seg.sum()/counter_nonezeros
        print("ave CT of all spine {}".format(ave_CT_all))

        ### 计算gth的平均
        saved_pth_label_seg = "calculate_label_CT"
        if not os.path.exists(saved_pth_label_seg):
            os.makedirs(saved_pth_label_seg)

        spine_mask_label = label.astype(bool).astype(np.int16)
        img_seg_label = img_or*spine_mask_label
        counter_nonezeros_label = np.count_nonzero(img_seg_label)
        ave_CT_all_gth = img_seg_label.sum()/counter_nonezeros_label
        print("ave CT of all spine in gth {}".format(ave_CT_all_gth))
        
        percentage_all = (ave_CT_all - ave_CT_all_gth)/ave_CT_all_gth
        print("percentage_all {}".format(percentage_all))
        global_percentage_all.append(percentage_all)


        ### 计算整个脊柱皮质和松质平均CT

        cirtex_mask = cortex_seg.astype(bool).astype(np.int16)
        cirtex_seg_or = img_or*cortex_seg
        counter_nonezeros = np.count_nonzero(cirtex_seg_or)
        ave_CT_cortex = cirtex_seg_or.sum()/counter_nonezeros
        print("ave CT of cortex spine {}".format(ave_CT_cortex))
        
        ###松质量

        Cancellous_seg_or = img_seg - cirtex_seg_or
        counter_nonezeros = np.count_nonzero(Cancellous_seg_or)
        ave_CT_Cancellous = Cancellous_seg_or.sum()/counter_nonezeros
        print("ave CT of Cancellous spine {}".format(ave_CT_Cancellous))

        ### 计算gth的
        ### 计算整个脊柱皮质和松质平均CT
        cirtex_mask_label = np.zeros_like(label)
        # cirtex_mask_label[label==1]=1
        for j in range(1,9):
            if(j%2!=0):
                cirtex_mask_label[label==j]=1

        cirtex_seg_label_or = img_or*cirtex_mask_label
        counter_nonezeros_label = np.count_nonzero(cirtex_seg_label_or)
        ave_CT_cortex_label = cirtex_seg_label_or.sum()/counter_nonezeros_label
        print("ave CT of cortex spine in gth {}".format(ave_CT_cortex_label))
        

        ###松质量
        Cancellous_mask_label = np.zeros_like(label)
        # Cancellous_mask_label[label==2]=1
        for j in range(1,9):
            if(j%2==0):
                Cancellous_mask_label[label==j]=1

        Cancellous_seg_or_label = img_or*Cancellous_mask_label
        counter_nonezeros_label = np.count_nonzero(Cancellous_seg_or_label)
        ave_CT_Cancellous_label = Cancellous_seg_or_label.sum()/counter_nonezeros_label
        print("ave CT of Cancellous spine in gth {}".format(ave_CT_Cancellous_label))

        percentage_cortex = (ave_CT_cortex-ave_CT_cortex_label)/ave_CT_cortex_label
        percentage_Cancellous = (ave_CT_Cancellous-ave_CT_Cancellous_label)/ave_CT_Cancellous_label
        print("percentage_cortex {},percentage_Cancellous {}".format(percentage_cortex,percentage_Cancellous))
        global_percentage_cortex.append(percentage_cortex)
        global_percentage_Cancellous.append(percentage_Cancellous)



##################绘图
global_percentage_all = np.array(global_percentage_all)
global_percentage_cortex = np.array(global_percentage_cortex)
global_percentage_Cancellous = np.array(global_percentage_Cancellous)
counter = global_percentage_all.size
x = np.arange(counter)
# y = np.array([6])
# scatter:绘制点，第1，2参数为坐标，s表示面积，c表示颜色，marker表示形状
plt.scatter(x, global_percentage_all, s=100, c='b', marker="*")
y_ = np.mean(global_percentage_all)
plt.axhline(y=y_, c="r", ls="--")
f = plt.gcf()  #获取当前图像
f.savefig(r'global_percentage_all_.png')
f.clear()  #释放内存

plt.scatter(x, global_percentage_cortex, s=100, c='b', marker="*")
y_ = np.mean(global_percentage_cortex)
plt.axhline(y=y_, c="r", ls="--")
f = plt.gcf()  #获取当前图像
f.savefig(r'global_percentage_cortex_.png')
f.clear()  #释放内存

plt.scatter(x, global_percentage_Cancellous, s=100, c='b', marker="*")
y_ = np.mean(global_percentage_Cancellous)
plt.axhline(y=y_, c="r", ls="--")
f = plt.gcf()  #获取当前图像
f.savefig(r'global_percentage_Cancellous_.png')
f.clear()  #释放内存

