###对皮质髓质进行计算miou
from metrics import runningScore, averageMeter
import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from collections import Counter
import cv2
from PIL import Image
import SimpleITK as sitk
running_metrics_val = runningScore(3)

# file_list = ["result_november","result_stage2"]
file_list = ["result_G0PA0"]

#分割参数
K_seg = 27
C_seg = -1
k_dili = 5
iter_dili = 6
miou_file_pth = "miou_benchmark.txt"

for file_list_n in file_list:


    label_root = "/root/Spine/Spine/Spine_segmentation/nnUnet_CTSpine1K/data/nnUNet_raw_data_base/nnUNet_raw_data/Task056_VerSe/{}/label".format(file_list_n)
    out_pth_root = "/root/Spine/Spine/Spine_segmentation/nnUnet_CTSpine1K/data/nnUNet_raw_data_base/nnUNet_raw_data/Task056_VerSe/{}/out_ct_begin_27_-1_20231228_2".format(file_list_n)
    seg_pred_root = "/root/Spine/Spine/Spine_segmentation/nnUnet_CTSpine1K/data/nnUNet_raw_data_base/nnUNet_raw_data/Task056_VerSe/{}/seg".format(file_list_n)

    print("processing "+file_list_n+"........................")

    seg_pred_file_root = os.listdir(seg_pred_root)
    for file in seg_pred_file_root:

        Gn = file.split("_")[1]
        PAn = file.split("_")[2]
        spine_seg_pth = os.path.join(seg_pred_root,file,PAn+".nii.gz")
        
        label_pth = os.path.join(label_root,Gn,PAn+".nii.gz")
        out_pth = os.path.join(out_pth_root,file,"{}{}_K{}C{}k{}i{}".format(Gn,PAn,str(K_seg),str(C_seg),str(k_dili),str(iter_dili)),"view_all_corte.nii.gz")
        print("processing "+Gn+" "+PAn)
        

        out_mask = sitk.ReadImage(out_pth)
        origin =out_mask.GetOrigin()
        direction = out_mask.GetDirection()
        space = out_mask.GetSpacing()
        out_mask = sitk.GetArrayFromImage(out_mask)

        label = sitk.ReadImage(label_pth)
        label = sitk.GetArrayFromImage(label)

        spine_seg = sitk.ReadImage(spine_seg_pth)
        spine_seg = sitk.GetArrayFromImage(spine_seg)

        slice_num = label.shape[0]

        ### 将label 处理为仅含0 1 ## 髓质，将非2的处理为0
        label_temp = np.zeros_like(label)   ##髓质的gth
        counter = []
        for i in range(slice_num):
            label_slice = label[i,:,:]

            for j in range(1,9):
                if(j%2==0):
                    k=2
                else:
                    k=1
                label_slice[label_slice==j]=k
            label_temp[i,:,:] = label_slice

            if(label_slice.max()>0):
                counter.append(i)

        out_s = np.zeros_like(label)
        gray_img_MASK = spine_seg.astype(bool).astype(np.int16)
        out_s[(gray_img_MASK>0)&(out_mask==0)] =2
        out_s[(gray_img_MASK>0)&(out_mask!=0)] =1
        ### iou计算函数

        time_meter = averageMeter()
        for i in counter:       ###仅对有label的通道进行计算
            running_metrics_val.update(label_temp[i,:,:] ,  out_s[i,:,:])
            
score, class_iou = running_metrics_val.get_scores()
print("score {}".format(score))
print("class_iou {}".format(class_iou))

with open(miou_file_pth,mode='a',encoding='utf-8') as f:
    f.write("score: \n"+str(score)+'\n')
    f.write("class_iou: \n"+str(class_iou))

f.close()
    
print("end")    

