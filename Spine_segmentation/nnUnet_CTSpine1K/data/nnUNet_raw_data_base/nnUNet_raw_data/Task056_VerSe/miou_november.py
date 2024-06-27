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
label_path_root = "result/label"
out_pth_root = "result/seg_out_finally"
spine_seg_pth_root = "result/spine_seg"
for i in range(3):
    label_pth = os.path.join(label_path_root,"dicom2PA{}_label.nii".format(i))
    out_pth = os.path.join(out_pth_root,'PA{}_k4i4_3_all.nii.gz'.format(i))
    spine_seg_pth = os.path.join(spine_seg_pth_root,"PA{}.nii.gz".format(i))


    out_mask = sitk.ReadImage(out_pth)
    origin =out_mask.GetOrigin()
    direction = out_mask.GetDirection()
    space = out_mask.GetSpacing()

    out_mask = sitk.GetArrayFromImage(out_mask)
    print(type(out_mask))
    print("out_mask shape:",out_mask.shape)
    slice_num = out_mask.shape[0]
    print(slice_num)

    label = sitk.ReadImage(label_pth)
    label = sitk.GetArrayFromImage(label)
    print(type(label))
    print("label shape:",label.shape)

    spine_seg = sitk.ReadImage(spine_seg_pth)
    spine_seg = sitk.GetArrayFromImage(spine_seg)
    print("spine_seg shape:",spine_seg.shape)


    slice_num = label.shape[0]
    print(slice_num)

    ### 将label 处理为仅含0 1 ## 髓质，将非2的处理为0
    label_temp = np.zeros_like(label)   ##髓质的gth
    counter = []
    for i in range(slice_num):
        label_slice = label[i,:,:]
        print("i == {},label {}".format(i,label_slice.max()))

        label_temp[i,:,:] = label_slice
        if(label_slice.max()>0&(spine_seg.max()>0)):
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
   
print("end")    