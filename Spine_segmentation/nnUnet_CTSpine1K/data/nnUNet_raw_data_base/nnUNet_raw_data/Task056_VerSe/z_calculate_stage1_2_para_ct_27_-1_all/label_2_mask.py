import os
import numpy as np
from tqdm import tqdm
import SimpleITK as sitk

file_list = ["result_november","result_stage2"]
K_seg = 27
C_seg = -1
k_dili = 5
iter_dili = 6

spine_id_l = [2,4,6,8]

for file_list_cur in file_list:
    seg_root = "/root/Spine/Spine/Spine_segmentation/nnUnet_CTSpine1K/data/nnUNet_raw_data_base/nnUNet_raw_data/Task056_VerSe/{}/label".format(file_list_cur)
    save_root = "/root/Spine/Spine/Spine_segmentation/nnUnet_CTSpine1K/data/nnUNet_raw_data_base/nnUNet_raw_data/Task056_VerSe/{}/label_seg".format(file_list_cur)
    seg_root_t = "/root/Spine/Spine/Spine_segmentation/nnUnet_CTSpine1K/data/nnUNet_raw_data_base/nnUNet_raw_data/Task056_VerSe/{}/seg".format(file_list_cur)
    
    for f in tqdm(os.listdir(seg_root_t)):
        Gn = f.split("_")[1]
        PAn = f.split("_")[2]
        PAn_file = "{}.nii.gz".format(PAn)
    # for file_n in tqdm(os.listdir(seg_root)):

        # Gn = file_n
        # P_f = os.path.join(seg_root,Gn)
        # for PAn_file in os.listdir(P_f):
        #     PAn = PAn_file.split(".")[0]
        file_path = os.path.join(seg_root,Gn,PAn+".nii.gz")
        # Gn = file_n.split("_")[-2]

        seg_file = sitk.ReadImage(file_path)
        origin =seg_file.GetOrigin()
        direction = seg_file.GetDirection()
        space = seg_file.GetSpacing()
        seg_file = sitk.GetArrayFromImage(seg_file)

        cancellous_mask = np.zeros_like(seg_file)
        for label_id in spine_id_l:
                cancellous_mask[seg_file==label_id]=1
        seg_file = cancellous_mask
            # seg_file[seg_file>21.5] = 0
            # seg_file[seg_file<17.5] = 0
            # seg_file[seg_file<0] = 0

        seg_file = seg_file.astype(bool).astype(np.int16)
        seg_file = sitk.GetImageFromArray(seg_file.astype(np.int16))
        seg_file.SetOrigin(origin)
        seg_file.SetDirection(direction)
        seg_file.SetSpacing(space)
            
        pth_cur = os.path.join(save_root,Gn)
        if not os.path.exists(pth_cur):
                os.makedirs(pth_cur)

        sitk.WriteImage(seg_file,os.path.join(pth_cur,PAn_file)) 