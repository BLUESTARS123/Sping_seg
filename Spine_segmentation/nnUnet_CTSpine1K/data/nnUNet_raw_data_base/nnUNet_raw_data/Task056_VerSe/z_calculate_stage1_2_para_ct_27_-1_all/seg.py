##
#分割皮质
#保存在save_root中
##

import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from collections import Counter
import cv2
from PIL import Image
import SimpleITK as sitk
from metrics import runningScore, averageMeter
from tqdm import tqdm
#


#数据读取模块

##根据需要修改下面的路径 
# file_list = ["result_november","result_stage2"]
file_list = ["result_G0PA0"]

#分割参数
K_seg = 27
C_seg = -1
k_dili = 5
iter_dili = 6

for file_list_n in file_list:
    label_root = "/root/Spine/Spine/Spine_segmentation/nnUnet_CTSpine1K/data/nnUNet_raw_data_base/nnUNet_raw_data/Task056_VerSe/{}/label".format(file_list_n)
    save_root = "/root/Spine/Spine/Spine_segmentation/nnUnet_CTSpine1K/data/nnUNet_raw_data_base/nnUNet_raw_data/Task056_VerSe/{}/out_ct_begin_27_-1_20231228_2".format(file_list_n)
    seg_pred_root = "/root/Spine/Spine/Spine_segmentation/nnUnet_CTSpine1K/data/nnUNet_raw_data_base/nnUNet_raw_data/Task056_VerSe/{}/seg".format(file_list_n)
    image_or_root = "/root/Spine/Spine/Spine_segmentation/nnUnet_CTSpine1K/data/nnUNet_raw_data_base/nnUNet_raw_data/Task056_VerSe/{}/img_o".format(file_list_n)
    print("processing "+file_list_n+"........................")

    seg_pred_file_root = os.listdir(seg_pred_root)
    for file in tqdm(seg_pred_file_root):
        Gn = file.split("_")[1]
        PAn = file.split("_")[2]

        seg_pred_file_path = os.path.join(seg_pred_root,file,PAn+".nii.gz")
        label_file_path = os.path.join(label_root,Gn,PAn+".nii.gz")
        image_file_path = os.path.join(image_or_root,"imagesTs_"+Gn+"_"+PAn,PAn+"_0000.nii.gz")
        # print("processing "+Gn+" "+PAn)

        #nnunet分割结果读取
        gth_pth = seg_pred_file_path
        img_PA0 = sitk.ReadImage(gth_pth)
        img_PA0 = sitk.GetArrayFromImage(img_PA0)

        
        #处理：只保留特定的脊柱节
        img_PA0[img_PA0>21.5] = 0
        img_PA0[img_PA0<17.5] = 0
        img_PA0[img_PA0<0] = 0
        
        # read raw img
        img_OR =  image_file_path
        img_OR_PA0 = sitk.ReadImage(img_OR)
        origin =img_OR_PA0.GetOrigin()
        direction = img_OR_PA0.GetDirection()
        space = img_OR_PA0.GetSpacing()
        img_OR_PA0 = sitk.GetArrayFromImage(img_OR_PA0)


        slice_num = img_OR_PA0.shape[0]

        
        # 生成y视角结果
        #[:,:,i] 侧面图 [:,i,:] 得到正面图 
        # 相关参数：阈值自适应参数：，；
        # 膨胀参数：kernal=（，），iterations = 

        z,x,y = img_OR_PA0.shape
        saved_pth_ = "{}{}_K{}C{}k{}i{}".format(Gn,PAn,str(K_seg),str(C_seg),str(k_dili),str(iter_dili))
        saved_pth = os.path.join(save_root,file,saved_pth_)
        if not os.path.exists(saved_pth):
            os.makedirs(saved_pth)

        

        out_y = np.zeros_like(img_OR_PA0)
        # out_seg_thread_y = np.zeros_like(img_OR_PA0)
        for i in range(y):
            img_slice = img_OR_PA0[:,:,i]
            img_slice[img_slice<0]=0
            img_slice=(img_slice/img_slice.max()*255).astype(np.uint8)
            img_slice = cv2.flip(img_slice, 0)

            temp = cv2.adaptiveThreshold(img_slice, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                cv2.THRESH_BINARY, K_seg,C_seg)
            # out_seg_thread_y[:,:,i] = temp

            slice_i = img_PA0[:,:,i]
            slice_i[slice_i<0]=0

            gray_img_MASK = slice_i.astype(bool).astype(np.int16)
            gray_img_MASK = cv2.flip(gray_img_MASK, 0)

            x = cv2.Sobel(gray_img_MASK*255, cv2.CV_16S, 1, 0)
            y = cv2.Sobel(gray_img_MASK*255, cv2.CV_16S, 0, 1)

            Scale_absX = cv2.convertScaleAbs(x)  # convert 转换  scale 缩放
            Scale_absY = cv2.convertScaleAbs(y)
            result = cv2.addWeighted(Scale_absX, 0.5, Scale_absY, 0.5, 0)
            dilate = cv2.dilate(result, kernel=(k_dili, k_dili), iterations=iter_dili)

            dilate_mask = dilate.astype(bool).astype(np.int16)
            finally_ = temp*gray_img_MASK*dilate_mask
            
            finally_mask = (temp*gray_img_MASK*dilate_mask).astype(bool).astype(np.int16)
            finally_mask =  cv2.flip(finally_mask, 0)
            out_y[:,:,i] = finally_mask
            out_y_tmp = out_y

        #y视角融合分割
        out_y = sitk.GetImageFromArray(out_y.astype(np.int16))
        out_y.SetOrigin(origin)
        out_y.SetDirection(direction)
        out_y.SetSpacing(space)
        sitk.WriteImage(out_y,os.path.join(saved_pth,'view_y.nii.gz')) 

        #y视角阈值分割
        # out_seg_thread_y =  sitk.GetImageFromArray(out_seg_thread_y.astype(np.int16))
        # out_seg_thread_y.SetOrigin(origin)
        # out_seg_thread_y.SetDirection(direction)
        # out_seg_thread_y.SetSpacing(space)

        # sitk.WriteImage(out_seg_thread_y,os.path.join(saved_pth,'view_y_thread.nii.gz')) 
        # print(" y end")     

        #### 生成Z视角结果
        
        z,x,y = img_OR_PA0.shape

        out_z = np.zeros_like(img_OR_PA0)
        # out_seg_thread_z = np.zeros_like(img_OR_PA0)
        for i in range(z):
            img_slice = img_OR_PA0[i,:,:]
            img_slice[img_slice<0]=0
            img_slice=(img_slice/img_slice.max()*255).astype(np.uint8)
            img_slice = cv2.flip(img_slice, 0)

            temp = cv2.adaptiveThreshold(img_slice, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                cv2.THRESH_BINARY, K_seg,C_seg)
            # out_seg_thread_z[i,:,:] = tmp
            slice_i = img_PA0[i,:,:]
            slice_i[slice_i<0]=0
            gray_img_MASK = slice_i.astype(bool).astype(np.int16)
            gray_img_MASK = cv2.flip(gray_img_MASK, 0)

            x = cv2.Sobel(gray_img_MASK*255, cv2.CV_16S, 1, 0)
            y = cv2.Sobel(gray_img_MASK*255, cv2.CV_16S, 0, 1)

            Scale_absX = cv2.convertScaleAbs(x)  # convert 转换  scale 缩放
            Scale_absY = cv2.convertScaleAbs(y)
            result = cv2.addWeighted(Scale_absX, 0.5, Scale_absY, 0.5, 0)
            dilate = cv2.dilate(result, kernel=(k_dili, k_dili), iterations=iter_dili)

            dilate_mask = dilate.astype(bool).astype(np.int16)
            finally_ = temp*gray_img_MASK*dilate_mask

            #保存temp*gray_img_MASK为仅有自适应阈值
            #保存完整finally_的yz视角为验证3d融合，仅有自适应阈值以及边缘位置先验
            #保存out为完整版本
            
            ###第一象限视角
            finally_mask = (temp*gray_img_MASK*dilate_mask).astype(bool).astype(np.int16)
            finally_mask =  cv2.flip(finally_mask, 0)
            out_z[i,:,:] = finally_mask
            out_z_tmp = out_z
        
        #z视角融合分割
        out_z = sitk.GetImageFromArray(out_z.astype(np.int16))
        out_z.SetOrigin(origin)
        out_z.SetDirection(direction)
        out_z.SetSpacing(space)
        sitk.WriteImage(out_z,os.path.join(saved_pth,'view_z.nii.gz')) 
        
        #z视角的阈值分割
        # out_seg_thread_z = sitk.GetImageFromArray(out_seg_thread_z.astype(np.int16))
        # out_seg_thread_z.SetOrigin(origin)
        # out_seg_thread_z.SetDirection(direction)
        # out_seg_thread_z.SetSpacing(space)
        # sitk.WriteImage(out_seg_thread_z,os.path.join(saved_pth,'view_z_thread.nii.gz'))              

        # print("z end")    


        #### 并集yz视角，生成all结果

        out_tmp = (out_z_tmp + out_y_tmp).astype(bool).astype(np.int16)
        out = sitk.GetImageFromArray(out_tmp.astype(np.int16))
        out.SetOrigin(origin)
        out.SetDirection(direction)
        out.SetSpacing(space)

        sitk.WriteImage(out,os.path.join(saved_pth,'view_all_corte.nii.gz'))        
        # print("end") 


        ##分割松质 
        # corte_mask = out_tmp.astype(bool)
        img_PA0[out_tmp==1]=0
        out_cancellous = img_PA0.astype(bool).astype(np.int16)
        out_cancellous = sitk.GetImageFromArray(out_cancellous.astype(np.int16))
        out_cancellous.SetOrigin(origin)
        out_cancellous.SetDirection(direction)
        out_cancellous.SetSpacing(space)

        sitk.WriteImage(out_cancellous,os.path.join(saved_pth,'view_all_cancellous.nii.gz')) 

print("end")




    




