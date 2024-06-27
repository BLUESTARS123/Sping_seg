
import os 
import numpy as np
# import SimpleITK as sitk
# from collections import Counter
import json

#绘图相关
import matplotlib.pyplot as plt

# import pandas as pd

ans_1 = np.load("ans_1_193.npy")
ans_2 = np.load("ans_2_193.npy")
ave1 = sum(ans_1)/len(ans_1)
ave2 = sum(ans_2)/len(ans_2)
ave_err = (ave2-ave1)/ave1
print("ave1 {}; ave2 {} ;ave_err {}".format(ave1,ave2,ave_err))

plt.xlabel('Serial Number of Valid Image Dataset (n=192)')  # x轴标题
plt.ylabel('Differences in Bone Mineral Density')  # y轴标题
num = len(ans_1)
x = [i for i in range(1,num+1)]
# plt.plot(x,ans_1,marker='o',label =" sampling group")
# plt.plot(x,ans_2,marker='x',label ="machine learning group")
plt.scatter(x,ans_1,marker='o',c="r",alpha=0.5,s=15,label =" S group")
plt.scatter(x,ans_2,marker='s',c = "dodgerblue",alpha=0.5,s=15,label ="ML group")
# plt.legend(["select","seg"])
plt.axhline(0,ls = '-.', c = 'k',label ="0")
plt.axhline(ave1,ls = '-.', c = 'firebrick',label ="mean S:{}".format(str(round(ave1, 3))))
plt.axhline(ave2,ls = '-.', c = 'royalblue',label ="mean ML:{}".format(str(round(ave2, 3))))
# plt.legend(loc="upper right",bbox_to_anchor=(1.05, 0))

plt.legend(bbox_to_anchor=(-0.05, 1),loc=3,ncol=3)
f = plt.gcf()  #获取当前图像
f.savefig(r'select_Gall_0126_4.png')
f.clear()  #释放内存