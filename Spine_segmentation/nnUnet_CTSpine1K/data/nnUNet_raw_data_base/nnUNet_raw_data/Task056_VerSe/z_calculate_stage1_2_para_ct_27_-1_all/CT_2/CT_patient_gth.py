###############################################################################################################
#计算一张图片的密度
import os 
import numpy as np
import SimpleITK as sitk
from collections import Counter
import json

from tqdm import tqdm

#分割参数
K_seg = 27
C_seg = -1
k_dili = 5
iter_dili = 6

spine_id_l = [18,19,20,21]
spine_id_can = [2,4,6,8]

file_list = ["result_november","result_stage2"]

ct_p = "./CT_patient_result_cancellous_gth"
# target_file_name = "view_all_cancellous.nii.gz"

if not os.path.exists(ct_p):
    os.makedirs(ct_p)

for file_list_n in file_list:

    spine_seg_root = "/root/Spine/Spine/Spine_segmentation/nnUnet_CTSpine1K/data/nnUNet_raw_data_base/nnUNet_raw_data/Task056_VerSe/{}/label".format(file_list_n)
    # cortex_seg_root = "/root/Spine/Spine/Spine_segmentation/nnUnet_CTSpine1K/data/nnUNet_raw_data_base/nnUNet_raw_data/Task056_VerSe/{}/out_ct_begin_27_-1_20231228_2".format(file_list_n)
    # cortex_seg_root = "/root/Spine/Spine/Spine_segmentation/nnUnet_CTSpine1K/data/nnUNet_raw_data_base/nnUNet_raw_data/Task056_VerSe/{}/label".format(file_list_n)
    img_or_root = "/root/Spine/Spine/Spine_segmentation/nnUnet_CTSpine1K/data/nnUNet_raw_data_base/nnUNet_raw_data/Task056_VerSe/{}/img_o".format(file_list_n)
    
    seg_root_t = "/root/Spine/Spine/Spine_segmentation/nnUnet_CTSpine1K/data/nnUNet_raw_data_base/nnUNet_raw_data/Task056_VerSe/{}/seg".format(file_list_n)
    # seg_pred_file_root = os.listdir(seg_root_t)
    for f in tqdm(os.listdir(seg_root_t)):
        Gn = f.split("_")[1]
        PAn = f.split("_")[2]
    # for file_n in tqdm(os.listdir(seg_pred_file_root)):

        # Gn = file_n
        # P_f = os.path.join(spine_seg_root,Gn)
        # for PAn_file in os.listdir(P_f):
        #     PAn = PAn_file.split(".")[0]
        spine_seg_pth = os.path.join(spine_seg_root,Gn,PAn+".nii.gz")
    
        img_or_path = os.path.join(img_or_root,"imagesTs_"+Gn+"_"+PAn,PAn+"_0000.nii.gz")
            # cortex_seg_path = os.path.join(cortex_seg_root,file,"{}{}_K{}C{}k{}i{}".format(Gn,PAn,str(K_seg),str(C_seg),str(k_dili),str(iter_dili)),target_file_name)
            # ct_f = os.path.join(ct_p,'{}.json'.format(file))
        file = "predict_{}_{}".format(Gn,PAn)
        ct_f2 = os.path.join(ct_p,'{}_py.json'.format(file))

        img = sitk.ReadImage(img_or_path)
        origin =img.GetOrigin()
        direction = img.GetDirection()
        space = img.GetSpacing()
        img = sitk.GetArrayFromImage(img)

        predict = sitk.ReadImage(spine_seg_pth)
        predict = sitk.GetArrayFromImage(predict)

        cancellous_mask = np.zeros_like(predict)
        for label_id in spine_id_can:
                cancellous_mask[predict==label_id]=1
        seg_file = cancellous_mask

        img_tmp = seg_file*img

            # out = sitk.ReadImage(cortex_seg_path)
            # out = sitk.GetArrayFromImage(out)

            # c,h,w = predict.shape
            # slice_num = predict.shape[0]
            ###################################
            # all_intensity = 0
            # all_counter_this_slice = 0
        all_intensity = img_tmp.sum()
        all_counter_this_slice = np.count_nonzero(img_tmp,axis=(0,1,2))
        mean_density = all_intensity/all_counter_this_slice


            # for spine_id in spine_id_l:
            #     spine_id_mask = np.zeros((c,h,w))
            #     spine_id_mask[predict==spine_id]=1
            #     img_tmp = spine_id_mask*out*img
                
            #     intensity = img_tmp.sum()
            #     counter_this_slice = np.count_nonzero(img_tmp,axis=(0,1,2))
            #     all_intensity+=intensity
            #     all_counter_this_slice+=counter_this_slice
                # density = intensity/counter_this_slice 
            # mean_density = all_intensity/all_counter_this_slice
        file_name = file
        file_path = os.path.join(spine_seg_root,file)
        spine_id = 0
        slice_num = 0
        json_list = {"file_name": file_name,"file_path": file_path,"spine_id": str(spine_id),"slice_num":int(slice_num),"density": float(mean_density),"sum_of_intensity_in_this_id": float(all_intensity),"pixel_num_in_this_id": int(all_counter_this_slice)}
    ###json for read
        #     for item  in json_list:
        # #         print(json_list[item])
        #         with open(ct_f, 'a+', encoding='utf-8') as fp:
        #             line = json.dumps({item:json_list[item]},ensure_ascii=False)
        #             fp.write(line + '\n')
        #     with open(ct_f, 'a+', encoding='utf-8') as fp:
        #             line = json.dumps("--------------------------------------------------------",ensure_ascii=False)
        #             fp.write(line + '\n')
            
            ###json for python
        with open(ct_f2, 'a+', encoding='utf-8') as fp:
                    line = json.dumps(json_list,ensure_ascii=False)
                    fp.write(line + '\n')
            
print("end")
    
