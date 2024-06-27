#dicon 转nii.gz
import SimpleITK as sitk
import numpy as np
import nibabel as nib
import os
import pandas as pd

import matplotlib.pyplot as plt

import shutil

def dcm2nii_sitk(path_read, path_save):
    reader = sitk.ImageSeriesReader()
    seriesIDs = reader.GetGDCMSeriesIDs(path_read)
    N = len(seriesIDs)
    lens = np.zeros([N])
    for i in range(N):
        dicom_names = reader.GetGDCMSeriesFileNames(path_read, seriesIDs[i])
        lens[i] = len(dicom_names)
    N_MAX = np.argmax(lens)
    dicom_names = reader.GetGDCMSeriesFileNames(path_read, seriesIDs[N_MAX])
    reader.SetFileNames(dicom_names)
    image = reader.Execute()
    if not os.path.exists(path_save):
        os.mkdir(path_save)
    sitk.WriteImage(image, path_save+'/data.nii.gz')


if __name__ == '__main__':

    # DICOMpath = "dataset/dicom_2023_benchmark/dicom_2023_benchmark"  #"dataset/dicom_all_spine_9_19/PA8/ST0"
    # Midpath = "dataset/dicom_2023_benchmark/middataset" #"dataset/dicom_all_spine_9_19/middataset1"
    # Resultpath = "dataset/dicom_2023_benchmark/result"#"dataset/dicom_all_spine_9_19/result"
    file_name = "G0"
    DICOMpath = "dataset/"+ file_name
    Midpath = "dataset/"+file_name+"_middataset" 
    Resultpath = "dataset/"+file_name+"_result"
    cases = os.listdir(DICOMpath)
    if not os.path.exists(Resultpath):
        os.mkdir(Resultpath)
    for c in cases:
        print("processing "+c)
        path_mid = os.path.join(DICOMpath, c)
        dcm2nii_sitk(path_mid, Midpath)
        shutil.copy(os.path.join(Midpath, "data.nii.gz"), os.path.join(Resultpath, c + "_0000.nii.gz"))


