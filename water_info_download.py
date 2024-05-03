

# 水情日报 数据下载
# Water information data download
# Version: 4.0
# Maintain on 2024.05.04



# Water information url
# (old) http://61.163.88.227:8006/hwsq.aspx?sr=0nkRxv6s9CTRMlwRgmfFF6jTpJPtAv87
# (new) http://61.163.88.227:8006/hwsq2.aspx?sr=0nkRxv6s9CTRMlwRgmfFF6jTpJPtAv87


# Design by HanLin

# BUG REPORT 2023.06.13:
# Something wrong in 2007.04.05, 2020.11.31, 2020.12.01!!!
# BUG has been fixed!

# # Start date (include)
# Start_date = '2003-05-20'
# # End date (include)
# End_date = '2003-06-24'

# Parameters start =======

# Start date (include)
Start_date = '2024-04-03'
# End date (include)
End_date = '2024-04-05'
# Result save path
# (Under the Download_data folder)
Save_path = r'./'

# Parameters end =======


import warnings
warnings.filterwarnings('ignore')


import os
import sys
import numpy as np
import pandas as pd
import bs4
from bs4 import BeautifulSoup
import requests
import datetime


Water_info_url=r'http://61.163.88.227:8006/hwsq2.aspx?sr=0nkRxv6s9CTRMlwRgmfFF6jTpJPtAv87'


# Initial login header
# In order to achieve cookie
header_first={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': '61.163.88.227:8006',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
}


# Secondary head
# In order to send a search request
header_next={
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': '61.163.88.227:8006',
    'Origin': r'http://61.163.88.227:8006',
    'Referer': 'http://61.163.88.227:8006/hwsq2.aspx?sr=0nkRxv6s9CTRMlwRgmfFF6jTpJPtAv87',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',

}


# Data to be transferred
# Use Form Data
postdata={
    'ctl00$ScriptManager1': 'ctl00$ScriptManager1|ctl00$ContentLeft$Button1',
    '__EVENTTARGET': '',
    '__EVENTARGUMENT': '',
    'ctl00$ContentLeft$menuDate1$TextBox11': '2024-04-12',
    '__VIEWSTATE':'/wEPDwULLTEwMDI5NzA1NzkPZBYCZg9kFgICAw9kFgICBQ9kFgJmD2QWAgIBD2QWAgIBDxYCHglpbm5lcmh0bWwF21o8dGFibGUgd2lkdGg9Ijk4JSIgYm9yZGVyPSIwIiBjZWxscGFkZGluZz0iMCIgY2VsbHNwYWNpbmc9IjEiIGJnY29sb3I9IiNEMUREQUEiIGFsaWduPSJjZW50ZXIiPjx0cj48dGQgaGVpZ2h0PSI0MCIgYmFja2dyb3VuZD0ic2tpbi9pbWFnZXMvbmV3bGluZWJnMy5naWYiPjx0YWJsZSB3aWR0aD0iOTglIiBib3JkZXI9IjAiIGNlbGxzcGFjaW5nPSIwIiBjZWxscGFkZGluZz0iMCI+PHRyPjx0ZCBhbGlnbj0iY2VudGVyIj48ZGl2IGNsYXNzPSdmaXJzdFRpdGxlJz7msLTmg4Xml6XmiqU8L2Rpdj48ZGl2IGNsYXNzPSdzZWNUaXRsZSc+MjAyMS0wNy0wNzwvZGl2PjwvdGQ+PC90cj48L3RhYmxlPjwvdGQ+PC90cj48L3RhYmxlPjx0YWJsZSB3aWR0aD0iOTglIiBib3JkZXI9IjAiIGNlbGxwYWRkaW5nPSIyIiBjZWxsc3BhY2luZz0iMSIgYmdjb2xvcj0iI0QxRERBQSIgYWxpZ249ImNlbnRlciIgc3R5bGU9Im1hcmdpbi10b3A6OHB4IiBjbGFzcz0ibWFpblR4dCI+PHRyPjx0ZCB3aWR0aD0iNTAlIj48dGFibGUgd2lkdGg9IjEwMCUiIGJvcmRlcj0iMCIgY2VsbHBhZGRpbmc9IjIiIGNlbGxzcGFjaW5nPSIxIiBiZ2NvbG9yPSIjRDFEREFBIiBhbGlnbj0iY2VudGVyIiBzdHlsZT0ibWFyZ2luLXRvcDo4cHgiIGNsYXNzPSJtYWluVHh0Ij48VFIgYWxpZ249J2NlbnRlcicgYmdjb2xvcj0nI0U3RTdFNycgaGVpZ2h0PScyMicgY2xhc3M9J3RhYmxlVGl0bGUnID48VEQgd2lkdGg9IjE1JSIgc3R5bGU9ImZvbnQtc2l6ZToxMXB0OyI+5rKz5ZCNPC9URD48VEQgd2lkdGg9IjI1JSIgc3R5bGU9ImZvbnQtc2l6ZToxMXB0OyI+56uZ5ZCNPC9URD48VEQgd2lkdGg9IjIwJSIgc3R5bGU9ImZvbnQtc2l6ZToxMXB0OyI+5rC05L2NPC9URD48VEQgd2lkdGg9IjIwJSIgc3R5bGU9ImZvbnQtc2l6ZToxMXB0OyI+5rWB6YePPC9URD48VEQgd2lkdGg9IjIwJSIgc3R5bGU9ImZvbnQtc2l6ZToxMXB0OyI+5ZCr5rKZ6YePPC9URD48L1RSPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuWUkOS5g+S6pSAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+MjY3Mi45OTwvdGQ+PHRkPjE0MzA8L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPum+mee+iuWzoeWFpeW6kzwvdGQ+PHRkPi08L3RkPjx0ZD4xNTEwPC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7pvpnnvorls6Hok4TmsLTph488L3RkPjx0ZD4yNTkwLjYxPC90ZD48dGQ+KDIwNSnkur88L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPum+mee+iuWzoeWHuuW6kzwvdGQ+PHRkPi08L3RkPjx0ZD4xMDYwPC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7liJjlrrbls6HlhaXlupM8L3RkPjx0ZD4tPC90ZD48dGQ+MTM0MDwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5YiY5a625bOh6JOE5rC06YePPC90ZD48dGQ+MTcyMS40MjwvdGQ+PHRkPigyMy43KeS6vzwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5YiY5a625bOh5Ye65bqTPC90ZD48dGQ+LTwvdGQ+PHRkPjExOTA8L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuWFsOW3niAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD4xNTExLjMzPC90ZD48dGQ+MTExMDwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5LiL5rKz5rK/ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD4xMjMwLjY4PC90ZD48dGQ+MTUwMDwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+55+z5Zi05bGxICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD4xMDg1Ljc1PC90ZD48dGQ+ODg2PC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7lt7Tlvabpq5jli5IgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD4xMDQ4Ljc0PC90ZD48dGQ+NDk1PC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7kuInmuZbmsrPlj6MgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD4xMDE2LjgyPC90ZD48dGQ+NTEyPC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7ljIXlpLQgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+MTAwMS41MzwvdGQ+PHRkPjQ2MDwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5aS06YGT5ouQICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD45ODYuNDU8L3RkPjx0ZD4zNzI8L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuS4h+WutuWvqOiThOawtOmHjzwvdGQ+PHRkPjk2MC44NDwvdGQ+PHRkPigxLjgzKeS6vzwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5LiH5a625a+o5LiK5Ye65bqTPC90ZD48dGQ+LTwvdGQ+PHRkPjQyNjwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5LiH5a625a+o5LiLICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+ODk5LjI1PC90ZD48dGQ+NDI2PC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7lupzosLcgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+ODA2LjU5PC90ZD48dGQ+MzI5PC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7lkLTloKEgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+NjM2LjE2PC90ZD48dGQ+NTMxPC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7pvpnpl6ggICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+Mzc3LjU0PC90ZD48dGQ+NjcxPC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPuaxvuaysyAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7msrPmtKUgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+LTwvdGQ+PHRkPi08L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+5YyX5rSb5rKzICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7nirblpLQgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+MzYwLjQzPC90ZD48dGQ+MS42NjwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7ms77msrMgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5byg5a625bGxICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD40MTkuNTk8L3RkPjx0ZD4yLjAyPC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPua4reaysyAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7lkrjpmLMgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+Mzc2LjY1PC90ZD48dGQ+MTI0PC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPua4reaysyAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7ljY7ljr8o5LqMKSAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPjMzNC4yOTwvdGQ+PHRkPjE4NjwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5r285YWzICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPjMyNi4xNzwvdGQ+PHRkPjczMjwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5Y+y5a625rup6JOE5rC06YePPC90ZD48dGQ+Mjg2Ljk8L3RkPjx0ZD4oMCnkur88L3RkPjx0ZD4tPC90ZD48L3RyPjwvdGFibGU+PC90ZD48dGQgd2lkdGg9IjUwJSI+PHRhYmxlIHdpZHRoPSIxMDAlIiBib3JkZXI9IjAiIGNlbGxwYWRkaW5nPSIyIiBjZWxsc3BhY2luZz0iMSIgYmdjb2xvcj0iI0QxRERBQSIgYWxpZ249ImNlbnRlciIgc3R5bGU9Im1hcmdpbi10b3A6OHB4IiBjbGFzcz0ibWFpblR4dCI+PFRSIGFsaWduPSdjZW50ZXInIGJnY29sb3I9JyNFN0U3RTcnIGhlaWdodD0nMjInIGNsYXNzPSd0YWJsZVRpdGxlJyA+PFREIHdpZHRoPSIxNSUiIHN0eWxlPSJmb250LXNpemU6MTFwdDsiPuays+WQjTwvVEQ+PFREIHdpZHRoPSIyNSUiIHN0eWxlPSJmb250LXNpemU6MTFwdDsiPuermeWQjTwvVEQ+PFREIHdpZHRoPSIyMCUiIHN0eWxlPSJmb250LXNpemU6MTFwdDsiPuawtOS9jTwvVEQ+PFREIHdpZHRoPSIyMCUiIHN0eWxlPSJmb250LXNpemU6MTFwdDsiPua1gemHjzwvVEQ+PFREIHdpZHRoPSIyMCUiIHN0eWxlPSJmb250LXNpemU6MTFwdDsiPuWQq+aymemHjzwvVEQ+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5LiJ6Zeo5bOhICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD4yNzMuOTk8L3RkPjx0ZD43OTY8L3RkPjx0ZD40OC43PC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuWwj+a1quW6leS4iuiThOawtOmHjzwvdGQ+PHRkPjIyMC45MjwvdGQ+PHRkPig0LjM4KeS6vzwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5bCP5rWq5bqVICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD4xMzUuMTU8L3RkPjx0ZD4yNjcwPC90ZD48dGQ+OS45NTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPuS8iuaysyAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7kuJzmub4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+MzYzLjAyPC90ZD48dGQ+NS41NTwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7kvIrmsrMgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+6ZmG5rWR5Z2d5LiK6JOE5rC06YePPC90ZD48dGQ+MzEzLjU4PC90ZD48dGQ+KDQuNDcp5Lq/PC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPuS8iuaysyAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7pmYbmtZHlnZ3kuIrlh7rlupM8L3RkPjx0ZD4tPC90ZD48dGQ+LTwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7kvIrmsrMgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+6b6Z6Zeo6ZWHICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD4xNDcuNTM8L3RkPjx0ZD4xNy44PC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPua0m+aysyAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7ljaLmsI8gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+NTQ5Ljg4PC90ZD48dGQ+MS40NDwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7mtJvmsrMgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5pWF5Y6/5rC05bqT6JOE5rC06YePPC90ZD48dGQ+NTE4Ljk4PC90ZD48dGQ+KDMuOTMp5Lq/PC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPua0m+aysyAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7mlYXljr/msLTlupPlh7rlupM8L3RkPjx0ZD4tPC90ZD48dGQ+LTwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7mtJvmsrMgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+6ZW/5rC077yI5LqM77yJICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPjM3Ny44NTwvdGQ+PHRkPjEuNjU8L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+5rSb5rKzICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPueZvemprOWvuiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+MTEyLjU0PC90ZD48dGQ+Ni45NjwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7kvIrmtJvmsrMgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPum7keefs+WFsyAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+MTA0LjM2PC90ZD48dGQ+NS45OTwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7kuLnmsrMgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5bGx6Lev5Z2qICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD4tPC90ZD48dGQ+LTwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7msoHmsrMgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5LqU6b6Z5Y+jICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD4xNDEuMjk8L3RkPjx0ZD40LjQwPC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPuaygeaysyAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7mrabpmZ8gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+OTguMjI8L3RkPjx0ZD4yLjE1PC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7oirHlm63lj6MgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPjg5Ljg1PC90ZD48dGQ+MjcxMDwvdGQ+PHRkPjMxLjU8L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5aS55rKz5rupICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD43Mi4yMzwvdGQ+PHRkPjI0MTA8L3RkPjx0ZD41NS4yPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPumrmOadkSAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD41OC43NTwvdGQ+PHRkPjI0MTA8L3RkPjx0ZD4zNi4yPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuWtmeWPoyAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD40NC43OTwvdGQ+PHRkPjI4MDA8L3RkPjx0ZD41LjA2PC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+5aSn5rG25rKzICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7miLTmnZHlnZ08L3RkPjx0ZD4tPC90ZD48dGQ+LTwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7kuJzlubPmuZYgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuS4nOW5s+a5luiAgea5luiThOawtOmHjzwvdGQ+PHRkPjQwLjYyPC90ZD48dGQ+KDMuOTYp5Lq/PC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPuWkp+axtuaysyAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5Ye65rmW6Ze4PC90ZD48dGQ+LTwvdGQ+PHRkPi08L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuiJvuWxsSAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD4zOC4zMTwvdGQ+PHRkPjI4ODA8L3RkPjx0ZD42LjUxPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuazuuWPoyAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD4yNi45NDwvdGQ+PHRkPjI2ODA8L3RkPjx0ZD43LjIwPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuWIqea0pSAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD4xMC42MTwvdGQ+PHRkPjI2MzA8L3RkPjx0ZD42LjgwPC90ZD48L3RyPjwvdGFibGU+PC90ZD48L3RyPjwvdGFibGU+ZGSSukZP4/WTcFFchShVyzOuLF6erAqG6y/c/i4jRc7t2g==',
    '__VIEWSTATEGENERATOR': '7E1BB901',
    '__EVENTVALIDATION': '/wEdAAO8xm3EeAEZxh8pNcnkCoprtFkthzWFWdRJPy8Ul6GtID9YyyR4qjX0bKJ2X6bXV1MRcIsu6/V+JRgxVsBqFVRhuSImD849azdAHMxdflWpyQ==',
    '__ASYNCPOST': 'true',
    'Button2': '查询',
}



# Parameters that don't seem to be useful
param={
    'sr': '0nkRxv6s9CTRMlwRgmfFF6jTpJPtAv87'
}


def Generate_date_list(start_date,end_date):

    date_lists=[]

    start_date=datetime.datetime.strptime(start_date,'%Y-%m-%d')
    end_date=datetime.datetime.strptime(end_date,'%Y-%m-%d')
    # Make sure the start time is less than the end time
    if start_date > end_date:
        print('Start time is greater than end time! ')
        sys.exit(0)
    else:
        while(start_date <= end_date):
            date_lists.append(datetime.datetime.strftime(start_date,'%Y-%m-%d'))
            start_date=start_date+datetime.timedelta(days=1)

    return date_lists


# Generate postdata corresponding to the date
def Generate_date_related_postdata(postdata,date):
    postdata['TextBox11']=date


# Update postdata
def Postdata_extraction(response,postdata):
    postdata_parameters=[
        '__VIEWSTATE',
        '__VIEWSTATEGENERATOR',
        '__EVENTVALIDATION',
        'TextBox11',
        'Button2'
        ]
    
    # Parsing html
    response = BeautifulSoup(response,'html.parser')

    # Data cleaning
    for single_response in response.find_all('input'):
        if isinstance(single_response,bs4.element.Tag):
            # 'type', 'name', 'id', 'value'
            if 'name' in single_response.attrs.keys():
                # Automatically fetch postdata parameters
                # __VIEWSTATE
                # __VIEWSTATEGENERATOR
                # __EVENTVALIDATION
                # TextBox11
                # Button2
                if single_response['name'] in postdata_parameters:
                    # name, id
                    single_response_name=single_response['name']
                    # value
                    single_response_value=single_response['value']
                    
                    # Null value is not updated
                    if not single_response_value=='':
                    
                        # postdata update
                        postdata.update({single_response_name:single_response_value})


def Information_extraction(response):

    response_lists=[]

    # Parsing html
    response = BeautifulSoup(response,'html.parser')

    # Data cleaning
    for row_index,single_response in enumerate(response.find_all('tr'),0):
        if len(single_response) == 5:
            if isinstance(single_response.contents[0],bs4.element.Tag):

                response_contents_lists=[]

                # Get child elements 0
                for column_index,single_response_content in enumerate(single_response.contents,0):
                    if isinstance(single_response_content,bs4.element.Tag):
                        # Get child elements 1
                        single_response_content_cache=single_response_content.contents[0]
                        # The format of the first column in the first row is different from the rest of the table! 
                        # The value of this cell is '河名' !
                        # The first column of the first row of the table. 
                        if row_index==0 and column_index==0:
                            # Final value
                            response_contents_lists.append(single_response_content_cache)
                        # The rest of the table. 
                        elif isinstance(single_response_content_cache,bs4.element.Tag):
                            # Get child elements 2
                            single_response_content_cache=single_response_content_cache.contents
                            if len(single_response_content_cache)!=0:
                                # Final value
                                response_contents_lists.append(single_response_content_cache[0])

                response_lists.append(response_contents_lists)

    return response_lists


def Generate_excel(information_lists):
    column_header=information_lists[0]
    Result_excel=pd.DataFrame(information_lists[1:],dtype=str,columns=column_header)


    return Result_excel


def Result_save(save_path,result_excel,date):

    dir_name = 'Download_data'

    file_path = os.path.join(save_path,dir_name)

    # Check if the folder is in
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    file_name = f'{date}.xlsx'

    file_path = os.path.join(file_path,file_name)

    result_excel.to_excel(file_path,header=True,index=True)


if __name__=='__main__':

    date_lists = Generate_date_list(Start_date,End_date)

    session = requests.session()
    
    # Step one: Establish connections and update postdata
    First_response = session.post(Water_info_url,headers=header_first)
    # 200: Success
    # 500: Failure
    First_response_status_code=First_response.status_code
    if First_response_status_code==200:
        
        First_response.raise_for_status()
        First_response.encoding = First_response.apparent_encoding
        # Get the returned postdata infomation
        First_response = First_response.text
        
        # Update Postdata
        Postdata_extraction(First_response,postdata)
        
        print(f'Postdata update success! ')
        
    else:
        # Internal Server Error
        print(f'Error, an internal server error occurred, program termination! ')
        # Program Termination
        sys.exit(0)

    # Step two: Use postdata to get water infomation
    for date_list in date_lists:
        
        # Writes the target date to the postdata
        Generate_date_related_postdata(postdata,date_list)

        Next_response = session.post(Water_info_url, headers=header_next, data=postdata)
        
        # 200: Success
        # 500: Failure
        Next_response_status_code=Next_response.status_code
        if Next_response_status_code==200:
            
            Next_response.raise_for_status()
            Next_response.encoding = Next_response.apparent_encoding
            # Get the returned infomation
            Next_response = Next_response.text
            
            # Detect empty pages
            # For example: '0|error|500||'
            if 'error' in Next_response and len(Next_response)<38:
                
                print(f'Date : {date_list} , an empty page detected, skip! ')
                continue
                
            else:
                # Normal
                Information_lists = Information_extraction(Next_response)
        
                Result_excel = Generate_excel(Information_lists)
        
                Result_save(Save_path,Result_excel,date_list)
        
                print(f'Date : {date_list} , data download is complete! ')
        
        else: 
            # Internal Server Error
            print(f'Date : {date_list} , an internal server error occurred, skip! ')
            continue
        








