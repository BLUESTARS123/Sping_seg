import os 
import numpy as np
import SimpleITK as sitk
from collections import Counter
import json

from tqdm import tqdm
import openpyxl
import matplotlib.pyplot as plt


def draw_scatter(mean_cBMD,class_n):
    if(class_n==1):
        plt.scatter(class_n,mean_cBMD,marker='o',c="firebrick",alpha=0.5,s=15,label =" class 0")
    elif(class_n==2):
        plt.scatter(class_n,mean_cBMD,marker='o',c="darkorange",alpha=0.5,s=15,label =" class 1")
    elif(class_n==3):
        plt.scatter(class_n,mean_cBMD,marker='o',c="limegreen",alpha=0.5,s=15,label =" class 2")
    elif(class_n==4):
        plt.scatter(class_n,mean_cBMD,marker='o',c="dodgerblue",alpha=0.5,s=15,label =" class 3")
    else:
        plt.scatter(class_n,mean_cBMD,marker='o',c="darkviolet",alpha=0.5,s=15,label =" class 4")

cbmd_r = "result_cancellous_with_mean.xlsx"
wb = openpyxl.load_workbook(cbmd_r)
# sheet = wb.active
sheet_list = wb.get_sheet_names()
print(sheet_list)

# excel_path = "result_spine.xlsx"
sheet_str = "Spine"

info = ["file_name","id_18","id_19","id_20","id_21"]



excel_list = []
name_list = []
# id1 = []
# id2 = []
id6 = []
id5 = []
sheet = wb["Spine"]
for cell in sheet['A']:
    name_list.append(cell.value)
name_list = name_list[1:]
# for cell in sheet['B']:
#     id1.append(cell.value)
# for cell in sheet['C']:
#     id2.append(cell.value)
# for cell in sheet['D']:
#     id3.append(cell.value)
for cell in sheet['F']:
    id5.append(cell.value)
for cell in sheet['G']:
    id6.append(cell.value)
id5 = id5[1:]
id6 = id6[1:]
print(name_list)

plt.xlabel('class number')  # x轴标题
plt.ylabel('cBMD')  # y轴标题

for id,f in tqdm(enumerate(name_list)):
    excel_list_cur = []
    excel_list_cur.append(f)

    mean_cBMD = id5[id]
    class_n = id6[id]
    draw_scatter(mean_cBMD,class_n)
plt.xlim([0,5])
plt.ylim([-0.3,-0.9])
# plt.legend(bbox_to_anchor=(-0.05, 1),loc=3,ncol=3)
# plt.legend()
f = plt.gcf()  #获取当前图像
f.savefig(r'class.png')
f.clear()  #释放内存
    


    



    # excel_list.append(excel_list_cur)
