#load json 计算流失比例
import os 
import numpy as np
import SimpleITK as sitk
from collections import Counter
import json

from tqdm import tqdm
import openpyxl

ct_r =  "./CT_patient_result_cancellous"
ct_benchmark_r = "./CT_benchmark_result_cancellous"
json_out = "./result_cancellous_with_mean"
if not os.path.exists(json_out):
    os.makedirs(json_out)

excel_path = "result_cancellous_with_mean.xlsx"
sheet_str = "Spine"

info = ["file_name","id_18","id_19","id_20","id_21","mean","class"]


file_benchmark = os.path.join(ct_benchmark_r,"predict_G0_PA0_py.json")

excel_list = []
cBMD_list = []
# cBMD_list_name = {}
def write_to_excel(path,sheet_str,info,data):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    data.insert(0,list(info))
    sheet.title = sheet_str

    for row_index, row_item in enumerate(data):

        for col_index, col_item in enumerate(row_item):
            sheet.cell(row=row_index+1,column= col_index+1,value=col_item)
    workbook.save(path)

# class_name_list = ["Normal bo"]
def check_class(mean_cBMD):
    if(mean_cBMD>=-0.2):
        return 1
    elif(mean_cBMD>=-0.5 and mean_cBMD<-0.2):
        return 2
    elif(mean_cBMD>=-0.7 and mean_cBMD<-0.5):
        return 3
    elif(mean_cBMD>=-0.9 and mean_cBMD<-0.7):
        return 4
    else:
        return 5




for file in tqdm(os.listdir(ct_r)):
    if(file.split(".")[-1]=="json" and file.split(".")[-2][-3:]=="_py"):
        PAn = file.split("_")[2]
        Gn = file.split("_")[1]
        file_t = os.path.join(ct_r,file)
        file_result = os.path.join(json_out,'{}_{}_cBMD.json'.format(Gn,PAn))
        PA0_filename = file_benchmark
        PA1_filename = file_t

        standard_dict = {}
        sum_of_intensity_dict = {}
        pixel_num_dict = {}
        file = open(PA0_filename, 'r', encoding='utf-8')
        for line in file.readlines():
            dic = json.loads(line)
            standard_dict[dic["spine_id"]]=dic["density"]
            sum_of_intensity_dict[dic["spine_id"]] = dic["sum_of_intensity_in_this_id"]
            pixel_num_dict[dic["spine_id"]]=dic["pixel_num_in_this_id"]
        # print(standard_dict)

        lv_dict={}
        lv_sum_of_intensity_dict = {}
        lv_pixel_num_dict = {}
        file = open(PA1_filename, 'r', encoding='utf-8')
        for line in file.readlines():
            dic = json.loads(line)
            lv_dict[dic["spine_id"]]=dic["density"]
            lv_sum_of_intensity_dict[dic["spine_id"]] = dic["sum_of_intensity_in_this_id"]
            lv_pixel_num_dict[dic["spine_id"]]=dic["pixel_num_in_this_id"]
        # print(lv_dict)
        cbmd_dict = {}
        
        all_intensity_patient = 0
        all_pixel_num_patient = 0
        all_intensity_pa0 = 0
        all_pixel_num_pa0 = 0
        for standard_id in standard_dict:
            
            if(standard_id in lv_dict):
                standard_density = standard_dict[standard_id]
                lv_density = lv_dict[standard_id]
                cBMD = (lv_density-standard_density)/standard_density
                cBMD = format(cBMD,'.2%')
                cbmd_dict[standard_id] = cBMD
                # cBMD_list.append(cBMD)
                all_intensity_patient+=lv_sum_of_intensity_dict[standard_id]
                all_pixel_num_patient+=lv_pixel_num_dict[standard_id]
                all_intensity_pa0+=sum_of_intensity_dict[standard_id]
                all_pixel_num_pa0+=pixel_num_dict[standard_id]
        mean_density_patient = all_intensity_patient/all_pixel_num_patient
        mean_density_pa0 = all_intensity_pa0/all_pixel_num_pa0
        mean_cBMD = (mean_density_patient-mean_density_pa0)/mean_density_pa0
        # mean_cBMD = format(mean_cBMD,'.2%')
        cbmd_dict["mean"] = mean_cBMD
        cbmd_dict["class"] = check_class(mean_cBMD)

        




        # print(cbmd_dict)

        #写入exel
        

        excel_list_cur = []
        excel_list_cur.append(Gn+"_"+PAn)
        for item  in cbmd_dict:
            excel_list_cur.append(cbmd_dict[item])
            with open(file_result, 'a+', encoding='utf-8') as fp:
                line = json.dumps({item:cbmd_dict[item]},ensure_ascii=False)
                fp.write(line + '\n')
        excel_list.append(excel_list_cur)

#写入exel
write_to_excel(excel_path,sheet_str,info,excel_list)

# ans_1 = np.array(ans_1)
# np.save('ans_1_193.npy',ans_1) 
