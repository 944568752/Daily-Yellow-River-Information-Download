

# 水情日报 数据下载
# Water information data download
# Version: 2.0


# Water information url
# http://61.163.88.227:8006/hwsq.aspx?sr=0nkRxv6s9CTRMlwRgmfFF6jTpJPtAv87


# Design by HanLin
# Something wrong in 2007.04.05, 2020.11.31, 2020.12.01!!!
# # Start date (include)
# Start_date = '2003-05-20'
# # End date (include)
# End_date = '2003-06-24'

# Parameters start =======

# Start date (include)
Start_date = '2007-04-04'
# End date (include)
End_date = '2007-04-06'
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


Water_info_url=r'http://61.163.88.227:8006/hwsq.aspx?sr=0nkRxv6s9CTRMlwRgmfFF6jTpJPtAv87'


# Initial login header
# In order to achieve cookie
header_first={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': '61.163.88.227:8006',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64',
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
    'Referer': 'http://61.163.88.227:8006/hwsq.aspx?sr=0nkRxv6s9CTRMlwRgmfFF6jTpJPtAv87',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37',

}


# Data to be transferred
# Use Form Data
postdata={
    'ctl00$ScriptManager1': 'ctl00$ScriptManager1|ctl00$ContentLeft$Button1',
    '__EVENTTARGET': '',
    '__EVENTARGUMENT': '',
    'ctl00$ContentLeft$menuDate1$TextBox11': '2022-06-13',
    '__VIEWSTATE':'/wEPDwULLTEwMDI5NzA1NzkPZBYCZg9kFgICAw9kFgICBQ9kFgJmD2QWAgIBD2QWAgIBDxYCHglpbm5lcmh0bWwF60w8dGFibGUgd2lkdGg9Ijk4JSIgYm9yZGVyPSIwIiBjZWxscGFkZGluZz0iMCIgY2VsbHNwYWNpbmc9IjEiIGJnY29sb3I9IiNEMUREQUEiIGFsaWduPSJjZW50ZXIiPjx0cj48dGQgaGVpZ2h0PSI0MCIgYmFja2dyb3VuZD0ic2tpbi9pbWFnZXMvbmV3bGluZWJnMy5naWYiPjx0YWJsZSB3aWR0aD0iOTglIiBib3JkZXI9IjAiIGNlbGxzcGFjaW5nPSIwIiBjZWxscGFkZGluZz0iMCI+PHRyPjx0ZCBhbGlnbj0iY2VudGVyIj48ZGl2IGNsYXNzPSdmaXJzdFRpdGxlJz7msLTmg4Xml6XmiqU8L2Rpdj48ZGl2IGNsYXNzPSdzZWNUaXRsZSc+MjAyMi0wNi0yNjwvZGl2PjwvdGQ+PC90cj48L3RhYmxlPjwvdGQ+PC90cj48L3RhYmxlPjx0YWJsZSB3aWR0aD0iOTglIiBib3JkZXI9IjAiIGNlbGxwYWRkaW5nPSIyIiBjZWxsc3BhY2luZz0iMSIgYmdjb2xvcj0iI0QxRERBQSIgYWxpZ249ImNlbnRlciIgc3R5bGU9Im1hcmdpbi10b3A6OHB4IiBjbGFzcz0ibWFpblR4dCI+PHRyPjx0ZCB3aWR0aD0iNTAlIj48dGFibGUgd2lkdGg9IjEwMCUiIGJvcmRlcj0iMCIgY2VsbHBhZGRpbmc9IjIiIGNlbGxzcGFjaW5nPSIxIiBiZ2NvbG9yPSIjRDFEREFBIiBhbGlnbj0iY2VudGVyIiBzdHlsZT0ibWFyZ2luLXRvcDo4cHgiIGNsYXNzPSJtYWluVHh0Ij48VFIgYWxpZ249J2NlbnRlcicgYmdjb2xvcj0nI0U3RTdFNycgaGVpZ2h0PScyMicgY2xhc3M9J3RhYmxlVGl0bGUnID48VEQgd2lkdGg9IjE1JSIgc3R5bGU9ImZvbnQtc2l6ZToxMXB0OyI+5rKz5ZCNPC9URD48VEQgd2lkdGg9IjI1JSIgc3R5bGU9ImZvbnQtc2l6ZToxMXB0OyI+56uZ5ZCNPC9URD48VEQgd2lkdGg9IjIwJSIgc3R5bGU9ImZvbnQtc2l6ZToxMXB0OyI+5rC05L2NPC9URD48VEQgd2lkdGg9IjIwJSIgc3R5bGU9ImZvbnQtc2l6ZToxMXB0OyI+5rWB6YePPC9URD48VEQgd2lkdGg9IjIwJSIgc3R5bGU9ImZvbnQtc2l6ZToxMXB0OyI+5ZCr5rKZ6YePPC9URD48L1RSPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7llJDkuYPkuqUgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD4yNjcxLjgxPC90ZD48dGQ+NzA2PC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+6b6Z576K5bOh5YWl5bqTPC90ZD48dGQ+LTwvdGQ+PHRkPjc0ODwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPum+mee+iuWzoeiThOawtOmHjzwvdGQ+PHRkPjI1ODMuNTg8L3RkPjx0ZD4oMTc5KeS6vzwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPum+mee+iuWzoeWHuuW6kzwvdGQ+PHRkPi08L3RkPjx0ZD4xMDYwPC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5YiY5a625bOh5YWl5bqTPC90ZD48dGQ+LTwvdGQ+PHRkPjEzMTA8L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7liJjlrrbls6Hok4TmsLTph488L3RkPjx0ZD4xNzE5LjM4PC90ZD48dGQ+KDIxLjgp5Lq/PC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5YiY5a625bOh5Ye65bqTPC90ZD48dGQ+LTwvdGQ+PHRkPjExMTA8L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7lhbDlt54gICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPjE1MTEuNjM8L3RkPjx0ZD4xMzUwPC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5LiL5rKz5rK/ICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+MTIzMC4yMjwvdGQ+PHRkPjExODA8L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7nn7PlmLTlsbEgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD4xMDg1Ljk3PC90ZD48dGQ+OTMwPC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5be05b2m6auY5YuSICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPjEwNDkuMDQ8L3RkPjx0ZD42MTE8L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7kuInmuZbmsrPlj6MgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+MTAxNi4zNTwvdGQ+PHRkPjMxNTwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuWMheWktCAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+MTAwMS4xODwvdGQ+PHRkPjI4MjwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuWktOmBk+aLkCAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPjk4NS41OTwvdGQ+PHRkPjIwNTwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuS4h+WutuWvqOiThOawtOmHjzwvdGQ+PHRkPjk3NS44OTwvdGQ+PHRkPig0Ljg1KeS6vzwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuS4h+WutuWvqOS4iuWHuuW6kzwvdGQ+PHRkPi08L3RkPjx0ZD4xMjwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuS4h+WutuWvqOS4iyAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD44OTguODc8L3RkPjx0ZD4xMjwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuW6nOiwtyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+ODA1Ljc2PC90ZD48dGQ+MTc0PC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5ZC05aChICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD42MzUuMTI8L3RkPjx0ZD4xNjY8L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7pvpnpl6ggICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPjM3Ni4xNTwvdGQ+PHRkPjE3MjwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7msb7msrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuays+a0pSAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+LTwvdGQ+PHRkPi08L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+5YyX5rSb5rKzICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+54q25aS0ICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD4zNjAuNTc8L3RkPjx0ZD41LjIyPC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPuazvuaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5byg5a625bGxICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+NDE5LjYxPC90ZD48dGQ+Mi40ODwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7muK3msrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuWSuOmYsyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+Mzc2LjIzPC90ZD48dGQ+NzkuNTwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7muK3msrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuWNjuWOvyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+MzM3LjQ1PC90ZD48dGQ+NDY8L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7mvbzlhbMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPjMyNC43NzwvdGQ+PHRkPjE4NTwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuWPsuWutua7qeiThOawtOmHjzwvdGQ+PHRkPjMxNi45PC90ZD48dGQ+KDUuMjgp5Lq/PC90ZD48dGQ+LTwvdGQ+PC90cj48L3RhYmxlPjwvdGQ+PHRkIHdpZHRoPSI1MCUiPjx0YWJsZSB3aWR0aD0iMTAwJSIgYm9yZGVyPSIwIiBjZWxscGFkZGluZz0iMiIgY2VsbHNwYWNpbmc9IjEiIGJnY29sb3I9IiNEMUREQUEiIGFsaWduPSJjZW50ZXIiIHN0eWxlPSJtYXJnaW4tdG9wOjhweCIgY2xhc3M9Im1haW5UeHQiPjxUUiBhbGlnbj0nY2VudGVyJyBiZ2NvbG9yPScjRTdFN0U3JyBoZWlnaHQ9JzIyJyBjbGFzcz0ndGFibGVUaXRsZScgPjxURCB3aWR0aD0iMTUlIiBzdHlsZT0iZm9udC1zaXplOjExcHQ7Ij7msrPlkI08L1REPjxURCB3aWR0aD0iMjUlIiBzdHlsZT0iZm9udC1zaXplOjExcHQ7Ij7nq5nlkI08L1REPjxURCB3aWR0aD0iMjAlIiBzdHlsZT0iZm9udC1zaXplOjExcHQ7Ij7msLTkvY08L1REPjxURCB3aWR0aD0iMjAlIiBzdHlsZT0iZm9udC1zaXplOjExcHQ7Ij7mtYHph488L1REPjxURCB3aWR0aD0iMjAlIiBzdHlsZT0iZm9udC1zaXplOjExcHQ7Ij7lkKvmspnph488L1REPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7kuInpl6jls6EgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD4yNzE8L3RkPjx0ZD4xNi40PC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5bCP5rWq5bqV5LiK6JOE5rC06YePPC90ZD48dGQ+MjQzLjY2PC90ZD48dGQ+KDI2LjYp5Lq/PC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5bCP5rWq5bqVICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+MTM2LjMxPC90ZD48dGQ+NDExMDwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7kvIrmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuS4nOa5viAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+MzYyLjU2PC90ZD48dGQ+Ny40MzwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7kvIrmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPumZhua1keWdneS4iuiThOawtOmHjzwvdGQ+PHRkPjMxMy41NDwvdGQ+PHRkPig0LjQ2KeS6vzwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7kvIrmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPumZhua1keWdneS4iuWHuuW6kzwvdGQ+PHRkPi08L3RkPjx0ZD4tPC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPuS8iuaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+6b6Z6Zeo6ZWHICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+MTQ3LjExPC90ZD48dGQ+MTMuNjwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7mtJvmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuWNouawjyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+NTQ5LjUzPC90ZD48dGQ+OS42MTwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7mtJvmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuaVheWOv+awtOW6k+iThOawtOmHjzwvdGQ+PHRkPjUxNy4xNDwvdGQ+PHRkPigzLjcxKeS6vzwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7mtJvmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuaVheWOv+awtOW6k+WHuuW6kzwvdGQ+PHRkPi08L3RkPjx0ZD4tPC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPua0m+aysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+6ZW/5rC077yI5LqM77yJICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD4zNzcuNzg8L3RkPjx0ZD4yMC41PC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPua0m+aysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+55m96ams5a+6ICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+MTEyLjY4PC90ZD48dGQ+MTYuNDwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7kvIrmtJvmsrMgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7pu5Hnn7PlhbMgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD4xMDQuMjY8L3RkPjx0ZD4yMi45PC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPuS4ueaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5bGx6Lev5Z2qICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+MTk5LjkyPC90ZD48dGQ+MC42ODY8L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+5rKB5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7kupTpvpnlj6MgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD4xNDAuNTk8L3RkPjx0ZD4xMDc8L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+5rKB5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7mrabpmZ8gICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPjEwMC4xNTwvdGQ+PHRkPjEwNzwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuiKseWbreWPoyAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPjkwLjUzPC90ZD48dGQ+NDEyMDwvdGQ+PHRkPioyLjM4PC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7lpLnmsrPmu6kgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD43Mi45MjwvdGQ+PHRkPjM4MTA8L3RkPjx0ZD4qMi42MjwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+6auY5p2RICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD41OS41NzwvdGQ+PHRkPjM3NjA8L3RkPjx0ZD4qMy44NTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5a2Z5Y+jICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD40NS4wODwvdGQ+PHRkPjMzNjA8L3RkPjx0ZD4qNC42NjwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPuWkp+axtuaysyAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuaItOadkeWdnTwvdGQ+PHRkPi08L3RkPjx0ZD4tPC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPuS4nOW5s+a5liAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuS4nOW5s+a5luiAgea5luiThOawtOmHjzwvdGQ+PHRkPjM5LjY4PC90ZD48dGQ+KDIuNTcp5Lq/PC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPuWkp+axtuaysyAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuWHuua5lumXuDwvdGQ+PHRkPi08L3RkPjx0ZD4tPC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+6Im+5bGxICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD4zOC40NDwvdGQ+PHRkPjMxNDA8L3RkPjx0ZD4qNi4zOTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5rO65Y+jICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD4yNi45NjwvdGQ+PHRkPjMwMjA8L3RkPjx0ZD4qNC4wMzwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5Yip5rSlICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD4xMC40PC90ZD48dGQ+MjcxMDwvdGQ+PHRkPio2Ljc4PC90ZD48L3RyPjwvdGFibGU+PC90ZD48L3RyPjwvdGFibGU+ZGQX7a8AK6EFHourJJ2xgJ7zGGznTXSzg7yZvMnSVM0/Mw==',
    '__VIEWSTATEGENERATOR': 'E4DC7756',
    '__EVENTVALIDATION': '/wEdAAPgMurU7dGbCJhtK8P1Nstr9DkLBAR+UXBBGQ1m5cY+HY5Ggl8DGIT46Qo2GBY6Yh4fpd+LHAI2ihOULO1i+2DgH5H5WRTn9WanmVpiptZGnA==',
    '__ASYNCPOST': 'true',
    'ctl00$ContentLeft$Button1': '查询',
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
    postdata['ctl00$ContentLeft$menuDate1$TextBox11']=date


def Information_extraction(response):

    response_lists=[]

    # Parsing html
    response = BeautifulSoup(response,'html.parser')

    # Data cleaning
    for single_response in response.find_all('tr'):
        if len(single_response) == 5:
            if isinstance(single_response.contents[0],bs4.element.Tag):

                response_contents_lists=[]

                for single_response_content in single_response.contents:
                    single_response_content_cache=single_response_content.contents
                    if len(single_response_content_cache)!=0:
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

    file_name = f'{date}.xls'

    file_path = os.path.join(file_path,file_name)

    result_excel.to_excel(file_path,header=True,index=True)


if __name__=='__main__':

    date_lists = Generate_date_list(Start_date,End_date)

    session = requests.session()
    First_response = session.post(Water_info_url,headers=header_first)

    for date_list in date_lists:

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
        








