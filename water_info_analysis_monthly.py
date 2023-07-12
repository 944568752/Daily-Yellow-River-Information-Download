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
Start_date = '2001-06'
# End date (include)
End_date = '2022-12'
# Site name on the website form
Site_name='利津'
# Water information data download folder
Data_download_path=r'C:\Users\Brian_Tsui\Desktop\git_temporary\Daily-Yellow-River-Information-Download\Download_data'
# Result save path
# (Under the Download_data folder)
Save_path = r'C:\Users\Brian_Tsui\Desktop\git_temporary\Daily-Yellow-River-Information-Download'

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


# Check if the folder is in
if not os.path.exists(Data_download_path):
    print('Data download path does not exist! ')
    # Program determination
    sys.exit(0)
    
# Obtain the file storage path
Save_path=os.path.join(Save_path,'Analysis_data')
if not os.path.exists(Save_path):
    os.makedirs(Save_path)


Date_cache=[]
# 数量统计(逐月)
Quantity_statistics_monthly=[]
# 水位
Water_level_cache=[]
# 流量
Flow_volume_cache=[]
# 含沙量
Sand_content_cache=[]


Start_year,Start_month=map(int,Start_date.split('-'))
End_year,End_month=map(int,End_date.split('-'))

Start_date=datetime.datetime.strptime(Start_date,'%Y-%m')
End_date=datetime.datetime.strptime(End_date,'%Y-%m')

for year in range(Start_year,End_year+1,1):
    if year==Start_year:
        month_start=Start_month
        month_end=13
    elif year==End_year:
        month_start=1
        month_end=End_month+1
    else:
        month_start=1
        month_end=13
        
    for month in range(month_start,month_end,1):
        month_date=datetime.datetime.strptime(f'{year}{month:0>2}','%Y%m')
        
        Date_cache.append(month_date)
        Quantity_statistics_monthly.append(0)
        Water_level_cache.append(0)
        Flow_volume_cache.append(0)
        Sand_content_cache.append(0)
        
        
for water_info_path in glob.glob(os.path.join(Data_download_path,'*.xls')):
    file_name=os.path.basename(water_info_path).split('.')[0]
    file_name=file_name[0:7]
    
    file_date=datetime.datetime.strptime(file_name,'%Y-%m')
    
    # Start_date =< file_date =< End_date
    if file_date>=Start_date and file_date<=End_date:
        print(f'Current file: {file_name}')
    else:
        # irrelevant data
        continue
    
    # Calculates the index of the current data in the cache list
    file_index=(file_date.year-Start_year)*12+(file_date.month-Start_month)
    
    # Data loading
    water_info=pd.read_excel(water_info_path,header=0,usecols=[2,3,4,5])
    water_info.iloc[:,0]=water_info.iloc[:,0].str.strip()
    
    target_keys=water_info.keys().tolist()
    target_row_index = water_info[water_info['站名'] == Site_name].index.tolist()[0]
    # print(target_row_index)
    
    target_row=water_info.iloc[target_row_index,:].tolist()

    try:    
        Water_level=float(target_row[1].replace('*',''))
        Flow_volume=float(target_row[2].replace('*',''))
        Sand_content=float(target_row[3].replace('*',''))
        
        # Valid data +1 
        Quantity_statistics_monthly[file_index]=Quantity_statistics_monthly[file_index]+1
        
        # print(f'站名: {Site_name}')
        # print(f'水位: {Water_level}')
        # print(f'流量: {Flow_volume}')
        # print(f'含沙量: {Sand_content}')
         
    except ValueError as e:
        Water_level=0
        Flow_volume=0
        Sand_content=0
        
        print('Invalid data exists! ')
        
    Water_level_cache[file_index]=Water_level_cache[file_index]+Water_level
    Flow_volume_cache[file_index]=Flow_volume_cache[file_index]+Flow_volume
    Sand_content_cache[file_index]=Sand_content_cache[file_index]+Sand_content
        

Quantity_statistics_monthly=np.array(Quantity_statistics_monthly,dtype=np.int32)
Quantity_statistics_monthly[Quantity_statistics_monthly==0]=1

# Calculate the monthly average data 
Water_level_cache=np.array(Water_level_cache,dtype=np.float32)/Quantity_statistics_monthly
Flow_volume_cache=np.array(Flow_volume_cache,dtype=np.float32)/Quantity_statistics_monthly
Sand_content_cache=np.array(Sand_content_cache,dtype=np.float32)/Quantity_statistics_monthly


# Analysis result saving
# np.save(os.path.join(Save_path,'Water_level_cache.npy'),Water_level_cache)
# np.save(os.path.join(Save_path,'Flow_volume_cache.npy'),Flow_volume_cache)
# np.save(os.path.join(Save_path,'Sand_content_cache.npy'),Sand_content_cache)

# Analysis result loading 
# Water_level_cache_path=os.path.join(Save_path,'Water_level_cache.npy')
# Flow_volume_cache_path=os.path.join(Save_path,'Flow_volume_cache.npy')
# Sand_content_cache_path=os.path.join(Save_path,'Sand_content_cache.npy')

# Water_level_cache=np.load(Water_level_cache_path)
# Flow_volume_cache=np.load(Flow_volume_cache_path)
# Sand_content_cache=np.load(Sand_content_cache_path)
        

# Generate X-axis coordinates
x_ticks_target_string=[str(Start_year)]
x_ticks_target_datetime=[datetime.datetime.strptime(str(Start_year),'%Y')]

for date in Date_cache:
    date=datetime.datetime.strftime(date,'%Y')
    if x_ticks_target_string[-1]!=date:
        x_ticks_target_string.append(date)
        
        date=datetime.datetime.strptime(date,'%Y')
        x_ticks_target_datetime.append(date)
        
# x_ticks_target=[datetime.datetime.strftime(date_time,'%Y') for date_time in Date_cache[::12]]


# Generate X-lim
# Start
if Start_month==1:
    x_lim_start_year=Start_year-1
    x_lim_start_month=12
else:
    x_lim_start_year=Start_year
    x_lim_start_month=Start_month-1

# End
if End_month==12:
    x_lim_end_year=End_year+1
    x_lim_end_month=1
else:
    x_lim_end_year=End_year
    x_lim_end_month=End_month-1
    

# Water level
fig=plt.figure(figsize=(120,20))
plt.rcParams['font.size']=42
plt.rcParams['font.sans-serif']=['Microsoft YaHei']

ax=plt.gca()
ax.spines['left'].set_linewidth(4)
ax.spines['right'].set_linewidth(4)
ax.spines['bottom'].set_linewidth(4)
ax.spines['top'].set_linewidth(4)

plt.axis('on')

plt.plot(Date_cache,Water_level_cache,color='red',linestyle='-',linewidth=4,marker='.',markersize=18)

plt.xticks(x_ticks_target_datetime,x_ticks_target_string,rotation=30)
plt.xlim(
    datetime.datetime.strptime(f'{x_lim_start_year}{x_lim_start_month:0>2}01','%Y%m%d'),
    datetime.datetime.strptime(f'{x_lim_end_year}{x_lim_end_month:0>2}01','%Y%m%d')
    )

plt.xlabel('时间（年）',labelpad=42)
plt.ylabel('水位（$km^{2}$）',labelpad=42)

plt.grid()
# plt.legend(facecolor='white',framealpha=1,loc='upper left')
plt.legend()
plt.savefig(os.path.join(Save_path,f'Water_Level_Analysis_Monthly.png'),bbox_inches='tight',pad_inches=0.08)
plt.clf()


# Flow volume
fig=plt.figure(figsize=(120,20))
plt.rcParams['font.size']=42
plt.rcParams['font.sans-serif']=['Microsoft YaHei']

ax=plt.gca()
ax.spines['left'].set_linewidth(4)
ax.spines['right'].set_linewidth(4)
ax.spines['bottom'].set_linewidth(4)
ax.spines['top'].set_linewidth(4)

plt.axis('on')

plt.plot(Date_cache,Flow_volume_cache,color='red',linestyle='-',linewidth=4,marker='.',markersize=18)

plt.xticks(x_ticks_target_datetime,x_ticks_target_string,rotation=30)
plt.xlim(
    datetime.datetime.strptime(f'{x_lim_start_year}{x_lim_start_month:0>2}01','%Y%m%d'),
    datetime.datetime.strptime(f'{x_lim_end_year}{x_lim_end_month:0>2}01','%Y%m%d')
    )

plt.xlabel('时间（年）',labelpad=42)
plt.ylabel('流量（$km^{2}$）',labelpad=42)

plt.grid()
# plt.legend(facecolor='white',framealpha=1,loc='upper left')
plt.legend()
plt.savefig(os.path.join(Save_path,f'Flow_Volume_Analysis_Monthly.png'),bbox_inches='tight',pad_inches=0.08)
plt.clf()


# Sand content
fig=plt.figure(figsize=(120,20))
plt.rcParams['font.size']=42
plt.rcParams['font.sans-serif']=['Microsoft YaHei']

ax=plt.gca()
ax.spines['left'].set_linewidth(4)
ax.spines['right'].set_linewidth(4)
ax.spines['bottom'].set_linewidth(4)
ax.spines['top'].set_linewidth(4)

plt.axis('on')

plt.plot(Date_cache,Sand_content_cache,color='red',linestyle='-',linewidth=4,marker='.',markersize=18)

plt.xticks(x_ticks_target_datetime,x_ticks_target_string,rotation=30)
plt.xlim(
    datetime.datetime.strptime(f'{x_lim_start_year}{x_lim_start_month:0>2}01','%Y%m%d'),
    datetime.datetime.strptime(f'{x_lim_end_year}{x_lim_end_month:0>2}01','%Y%m%d')
    )

plt.xlabel('时间（年）',labelpad=42)
plt.ylabel('含沙量（$km^{2}$）',labelpad=42)

plt.grid()
# plt.legend(facecolor='white',framealpha=1,loc='upper left')
plt.legend()
plt.savefig(os.path.join(Save_path,f'Sand_Content_Analysis_Monthly.png'),bbox_inches='tight',pad_inches=0.08)
plt.clf()




