import os
import numpy as np
from tqdm import tqdm
import SimpleITK as sitk

file_list = ["result_november","result_stage2","result_G0PA0"]
K_seg = 27
C_seg = -1
k_dili = 5
iter_dili = 6

for file_list_cur in file_list:
    seg_root = "/root/Spine/Spine/Spine_segmentation/nnUnet_CTSpine1K/data/nnUNet_raw_data_base/nnUNet_raw_data/Task056_VerSe/{}/seg".format(file_list_cur)
    save_root = "/root/Spine/Spine/Spine_segmentation/nnUnet_CTSpine1K/data/nnUNet_raw_data_base/nnUNet_raw_data/Task056_VerSe/{}/seg_mask".format(file_list_cur)
    

    for file_n in tqdm(os.listdir(seg_root)):
        PAn = file_n.split("_")[-1]
        file_path = os.path.join(seg_root,file_n,PAn+".nii.gz")
        Gn = file_n.split("_")[-2]

        seg_file = sitk.ReadImage(file_path)
        origin =seg_file.GetOrigin()
        direction = seg_file.GetDirection()
        space = seg_file.GetSpacing()
        seg_file = sitk.GetArrayFromImage(seg_file)

        seg_file[seg_file>21.5] = 0
        seg_file[seg_file<17.5] = 0
        seg_file[seg_file<0] = 0

        seg_file = seg_file.astype(bool).astype(np.int16)
        seg_file = sitk.GetImageFromArray(seg_file.astype(np.int16))
        seg_file.SetOrigin(origin)
        seg_file.SetDirection(direction)
        seg_file.SetSpacing(space)
        
        pth_cur = os.path.join(save_root,file_n,"{}{}_K{}C{}k{}i{}".format(Gn,PAn,str(K_seg),str(C_seg),str(k_dili),str(iter_dili)))
        if not os.path.exists(pth_cur):
            os.makedirs(pth_cur)

        sitk.WriteImage(seg_file,os.path.join(pth_cur,"view_all_spine.nii.gz")) 