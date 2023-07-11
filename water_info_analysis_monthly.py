# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 00:37:42 2023

@author: Brian_Tsui
"""


# 水情日报 数据分析(逐月)
# Water information data analysis (monthly)
# Version: 2.0


# Water information url
# http://61.163.88.227:8006/hwsq.aspx?sr=0nkRxv6s9CTRMlwRgmfFF6jTpJPtAv87


# Design by HanLin


# Parameters start =======

# Start date (include)
Start_date = '2001-04'
# End date (include)
End_date = '2022-06'
# Site name on the website form
Site_name='利津'
# Water information data download folder
Data_download_path=r'./Download_data'
# Result save path
# (Under the Download_data folder)
Save_path = r'./'

# Parameters end =======


import warnings
warnings.filterwarnings('ignore')


import os
import sys
import glob
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt


Date_cache=[]
# 数量统计(逐月)
Quantity_statistics_monthly=[]
# 水位
Water_level_cache=[]
# 流量
Flow_volume_cache=[]
# 含沙量
Sand_content_cache=[]


for year in range(2000,2023,1):
    for month in range(1,12,1):
        month_date=datetime.datetime.strptime(f'{year}{month:0>2}','%Y%m')
        
        Date_cache.append(month_date)
        Quantity_statistics_monthly.append(0)
        Water_level_cache.append(0)
        Flow_volume_cache.append(0)
        Sand_content_cache.append(0)
        
        
for path in glob.glob(os.path.join(Data_download_path,'*.xls')):
    file_name=os.path.basename(path).split('.')[0]
    file_name=file_name[0:7]
    print(file_name)
    
    file_date=datetime.datetime.strptime(file_name,'%Y-%m')
    file_index=(file_date.year-2000)*12+file_date.month-1
    
    # if len(Date_cache)==0:
    #     Date_cache.append(file_date)
    #     wl_cache.append(0)
    #     fv_cache.append(0)
    #     sc_cache.append(0)
    # elif Date_cache[-1]!=file_date:
    #     Date_cache.append(file_date)
        
    #     if Monthly_quantity_statistics!=0:
    #         wl_cache[-1]=wl_cache[-1]/Monthly_quantity_statistics
    #         fv_cache[-1]=fv_cache[-1]/Monthly_quantity_statistics
    #         sc_cache[-1]=sc_cache[-1]/Monthly_quantity_statistics
            
    #     Monthly_quantity_statistics=0
        
    #     wl_cache.append(0)
    #     fv_cache.append(0)
    #     sc_cache.append(0)

    water_info=pd.read_excel(path,header=0,usecols=[2,3,4,5])
    water_info.iloc[:,0]=water_info.iloc[:,0].str.strip()
    
    target_keys=water_info.keys().tolist()
    target_row_index = water_info[water_info['站名'] == Site_name].index.tolist()[0]
    # print(target_row_index)
    
    target_row=water_info.iloc[target_row_index,:].tolist()

    try:    
        Water_level=float(target_row[1])
        Flow_volume=float(target_row[2])
        Sand_content=float(target_row[3])

        Water_level_cache[file_index]=Water_level_cache[file_index]+Water_level
        Flow_volume_cache[file_index]=Flow_volume_cache[file_index]+Flow_volume
        Sand_content_cache[file_index]=Sand_content_cache[file_index]+Sand_content
        
        Quantity_statistics_monthly[file_index]=Quantity_statistics_monthly[file_index]+1
        
        # print(f'站名: {Site_name}')
        # print(f'水位: {Water_level}')
        # print(f'流量: {Flow_volume}')
        # print(f'含沙量: {Sand_content}')
    except ValueError as e:
        # print('Invalid data! ')
        Water_level=0
        Flow_volume=0
        Sand_content=0
        

Quantity_statistics_monthly=np.array(Quantity_statistics_monthly,dtype=np.int32)
Quantity_statistics_monthly[Quantity_statistics_monthly==0]=1

Water_level_cache=np.array(Water_level_cache,dtype=np.float32)/Quantity_statistics_monthly
Flow_volume_cache=np.array(Flow_volume_cache,dtype=np.float32)/Quantity_statistics_monthly
Sand_content_cache=np.array(Sand_content_cache,dtype=np.float32)/Quantity_statistics_monthly


np.save(os.path.join(Save_path,'wl_cache.npy'),Water_level_cache)
np.save(os.path.join(Save_path,'fv_cache.npy'),Flow_volume_cache)
np.save(os.path.join(Save_path,'sc_cache.npy'),Sand_content_cache)




wl_cache_path=os.path.join(Result_path,'wl_cache.npy')
fv_cache_path=os.path.join(Result_path,'fv_cache.npy')
sc_cache_path=os.path.join(Result_path,'sc_cache.npy')

wl_cache=np.load(wl_cache_path)
fv_cache=np.load(fv_cache_path)
sc_cache=np.load(sc_cache_path)

Date_cache=[]
for year in range(2000,2023,1):
    for month in range(1,13,1):
        month_date=datetime.datetime.strptime(f'{year}{month:0>2}','%Y%m')
        Date_cache.append(month_date)
        
        
x_ticks_target=[datetime.datetime.strftime(date_time,'%Y') for date_time in Date_cache[::12]]



fig=plt.figure(figsize=(120,20))
plt.rcParams['font.size']=42
plt.rcParams['font.sans-serif']=['Microsoft YaHei']

ax=plt.gca()
ax.spines['left'].set_linewidth(4)
ax.spines['right'].set_linewidth(4)
ax.spines['bottom'].set_linewidth(4)
ax.spines['top'].set_linewidth(4)

plt.axis('on')

plt.plot(Date_cache,wl_cache,color='red',linestyle='-',linewidth=4,marker='.',markersize=18)
plt.xticks(Date_cache[::12],[datetime.datetime.strftime(date_time,'%Y') for date_time in Date_cache[::12]],rotation=30)
plt.xlim(datetime.datetime.strptime('19991201','%Y%m%d'),datetime.datetime.strptime('20230101','%Y%m%d'))

plt.xlabel('时间（年）',labelpad=42)
plt.ylabel('水位（$km^{2}$）',labelpad=42)

plt.grid()
# plt.legend(facecolor='white',framealpha=1,loc='upper left')
plt.legend()
plt.savefig(os.path.join(Result_path,f'WL_Analysis_Annual_only_target.png'),bbox_inches='tight',pad_inches=0.08)
plt.clf()


fig=plt.figure(figsize=(120,20))
plt.rcParams['font.size']=42
plt.rcParams['font.sans-serif']=['Microsoft YaHei']

ax=plt.gca()
ax.spines['left'].set_linewidth(4)
ax.spines['right'].set_linewidth(4)
ax.spines['bottom'].set_linewidth(4)
ax.spines['top'].set_linewidth(4)

plt.axis('on')

plt.plot(Date_cache,fv_cache,color='red',linestyle='-',linewidth=4,marker='.',markersize=18)
plt.xticks(Date_cache[::12],[datetime.datetime.strftime(date_time,'%Y') for date_time in Date_cache[::12]],rotation=30)
plt.xlim(datetime.datetime.strptime('19991201','%Y%m%d'),datetime.datetime.strptime('20230101','%Y%m%d'))

plt.xlabel('时间（年）',labelpad=42)
plt.ylabel('流量（$km^{2}$）',labelpad=42)

plt.grid()
# plt.legend(facecolor='white',framealpha=1,loc='upper left')
plt.legend()
plt.savefig(os.path.join(Result_path,f'FV_Analysis_Annual_only_target.png'),bbox_inches='tight',pad_inches=0.08)
plt.clf()


fig=plt.figure(figsize=(120,20))
plt.rcParams['font.size']=42
plt.rcParams['font.sans-serif']=['Microsoft YaHei']

ax=plt.gca()
ax.spines['left'].set_linewidth(4)
ax.spines['right'].set_linewidth(4)
ax.spines['bottom'].set_linewidth(4)
ax.spines['top'].set_linewidth(4)

plt.axis('on')

plt.plot(Date_cache,sc_cache,color='red',linestyle='-',linewidth=4,marker='.',markersize=18)
plt.xticks(Date_cache[::12],[datetime.datetime.strftime(date_time,'%Y') for date_time in Date_cache[::12]],rotation=30)
plt.xlim(datetime.datetime.strptime('19991201','%Y%m%d'),datetime.datetime.strptime('20230101','%Y%m%d'))

plt.xlabel('时间（年）',labelpad=42)
plt.ylabel('含沙量（$km^{2}$）',labelpad=42)

plt.grid()
# plt.legend(facecolor='white',framealpha=1,loc='upper left')
plt.legend()
plt.savefig(os.path.join(Result_path,f'SC_Analysis_Annual_only_target.png'),bbox_inches='tight',pad_inches=0.08)
plt.clf()























