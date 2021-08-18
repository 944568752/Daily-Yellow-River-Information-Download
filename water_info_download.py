

# 水情日报 数据下载
# Water information data download


# Water information url
# http://61.163.88.227:8006/hwsq.aspx?sr=0nkRxv6s9CTRMlwRgmfFF6jTpJPtAv87


# Design by HanLin


# Parameters start =======

# Start date (include)
Start_date = '2021-06-01'
# End date (include)
End_date = '2021-07-06'
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
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64',
}


# Data to be transferred
# Use Form Data
postdata={
    'ctl00$ScriptManager1': 'ctl00$ScriptManager1|ctl00$ContentLeft$Button1',
    '__EVENTTARGET': '',
    '__EVENTARGUMENT': '',
    'ctl00$ContentLeft$menuDate1$TextBox11': '2020-06-13',
    '__VIEWSTATE':'/wEPDwULLTEwMDI5NzA1NzkPZBYCZg9kFgICAw9kFgICBQ9kFgJmD2QWAgIBD2QWAgIBDxYCHglpbm5lcmh0bWwF7Ew8dGFibGUgd2lkdGg9Ijk4JSIgYm9yZGVyPSIwIiBjZWxscGFkZGluZz0iMCIgY2VsbHNwYWNpbmc9IjEiIGJnY29sb3I9IiNEMUREQUEiIGFsaWduPSJjZW50ZXIiPjx0cj48dGQgaGVpZ2h0PSI0MCIgYmFja2dyb3VuZD0ic2tpbi9pbWFnZXMvbmV3bGluZWJnMy5naWYiPjx0YWJsZSB3aWR0aD0iOTglIiBib3JkZXI9IjAiIGNlbGxzcGFjaW5nPSIwIiBjZWxscGFkZGluZz0iMCI+PHRyPjx0ZCBhbGlnbj0iY2VudGVyIj48ZGl2IGNsYXNzPSdmaXJzdFRpdGxlJz7msLTmg4Xml6XmiqU8L2Rpdj48ZGl2IGNsYXNzPSdzZWNUaXRsZSc+MjAyMS0wNy0wMTwvZGl2PjwvdGQ+PC90cj48L3RhYmxlPjwvdGQ+PC90cj48L3RhYmxlPjx0YWJsZSB3aWR0aD0iOTglIiBib3JkZXI9IjAiIGNlbGxwYWRkaW5nPSIyIiBjZWxsc3BhY2luZz0iMSIgYmdjb2xvcj0iI0QxRERBQSIgYWxpZ249ImNlbnRlciIgc3R5bGU9Im1hcmdpbi10b3A6OHB4IiBjbGFzcz0ibWFpblR4dCI+PHRyPjx0ZCB3aWR0aD0iNTAlIj48dGFibGUgd2lkdGg9IjEwMCUiIGJvcmRlcj0iMCIgY2VsbHBhZGRpbmc9IjIiIGNlbGxzcGFjaW5nPSIxIiBiZ2NvbG9yPSIjRDFEREFBIiBhbGlnbj0iY2VudGVyIiBzdHlsZT0ibWFyZ2luLXRvcDo4cHgiIGNsYXNzPSJtYWluVHh0Ij48VFIgYWxpZ249J2NlbnRlcicgYmdjb2xvcj0nI0U3RTdFNycgaGVpZ2h0PScyMicgY2xhc3M9J3RhYmxlVGl0bGUnID48VEQgd2lkdGg9IjE1JSIgc3R5bGU9ImZvbnQtc2l6ZToxMXB0OyI+5rKz5ZCNPC9URD48VEQgd2lkdGg9IjI1JSIgc3R5bGU9ImZvbnQtc2l6ZToxMXB0OyI+56uZ5ZCNPC9URD48VEQgd2lkdGg9IjIwJSIgc3R5bGU9ImZvbnQtc2l6ZToxMXB0OyI+5rC05L2NPC9URD48VEQgd2lkdGg9IjIwJSIgc3R5bGU9ImZvbnQtc2l6ZToxMXB0OyI+5rWB6YePPC9URD48VEQgd2lkdGg9IjIwJSIgc3R5bGU9ImZvbnQtc2l6ZToxMXB0OyI+5ZCr5rKZ6YePPC9URD48L1RSPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7llJDkuYPkuqUgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD4yNjczLjU1PC90ZD48dGQ+MTgyMDwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPum+mee+iuWzoeWFpeW6kzwvdGQ+PHRkPi08L3RkPjx0ZD4xODcwPC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+6b6Z576K5bOh6JOE5rC06YePPC90ZD48dGQ+MjU4OS43NjwvdGQ+PHRkPigyMDIp5Lq/PC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+6b6Z576K5bOh5Ye65bqTPC90ZD48dGQ+LTwvdGQ+PHRkPjEwNzA8L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7liJjlrrbls6HlhaXlupM8L3RkPjx0ZD4tPC90ZD48dGQ+MTIzMDwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuWImOWutuWzoeiThOawtOmHjzwvdGQ+PHRkPjE3MjEuMzE8L3RkPjx0ZD4oMjMuNinkur88L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7liJjlrrbls6Hlh7rlupM8L3RkPjx0ZD4tPC90ZD48dGQ+MTE1MDwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuWFsOW3niAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+MTUxMS45PC90ZD48dGQ+MTU1MDwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuS4i+ays+ayvyAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPjEyMzAuNTY8L3RkPjx0ZD4xNDEwPC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+55+z5Zi05bGxICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+MTA4NS42PC90ZD48dGQ+NzkwPC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5be05b2m6auY5YuSICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPjEwNDguNDk8L3RkPjx0ZD4zOTA8L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7kuInmuZbmsrPlj6MgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+MTAxNi4zOTwvdGQ+PHRkPjM2NjwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuWMheWktCAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+MTAwMS4xODwvdGQ+PHRkPjMyMjwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuWktOmBk+aLkCAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPjk4Ni4xNDwvdGQ+PHRkPjI5NjwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuS4h+WutuWvqOiThOawtOmHjzwvdGQ+PHRkPjk2OS44NjwvdGQ+PHRkPigzLjIxKeS6vzwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuS4h+WutuWvqOS4iuWHuuW6kzwvdGQ+PHRkPi08L3RkPjx0ZD4xMjYwPC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5LiH5a625a+o5LiLICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPjkwMC4yNjwvdGQ+PHRkPjEyNjA8L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7lupzosLcgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPjgwOC4zNzwvdGQ+PHRkPjEwMTA8L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7lkLTloKEgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPjYzNS44PC90ZD48dGQ+Mzc4PC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+6b6Z6ZeoICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD4zNzYuNjg8L3RkPjx0ZD4zMTE8L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+5rG+5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7msrPmtKUgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPi08L3RkPjx0ZD4tPC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPuWMl+a0m+aysyAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPueKtuWktCAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+MzYwLjU2PC90ZD48dGQ+NC43ODwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7ms77msrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuW8oOWutuWxsSAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPjQxOS42OTwvdGQ+PHRkPjYuMDI8L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+5rit5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7lkrjpmLMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPjM3Ni42NjwvdGQ+PHRkPjEwNTwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7muK3msrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuWNjuWOvyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+MzM0LjA0PC90ZD48dGQ+MTQ5PC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5r285YWzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD4zMjUuMzc8L3RkPjx0ZD4zNDI8L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7lj7Llrrbmu6nok4TmsLTph488L3RkPjx0ZD4zMTYuNjE8L3RkPjx0ZD4oNC41MSnkur88L3RkPjx0ZD4tPC90ZD48L3RyPjwvdGFibGU+PC90ZD48dGQgd2lkdGg9IjUwJSI+PHRhYmxlIHdpZHRoPSIxMDAlIiBib3JkZXI9IjAiIGNlbGxwYWRkaW5nPSIyIiBjZWxsc3BhY2luZz0iMSIgYmdjb2xvcj0iI0QxRERBQSIgYWxpZ249ImNlbnRlciIgc3R5bGU9Im1hcmdpbi10b3A6OHB4IiBjbGFzcz0ibWFpblR4dCI+PFRSIGFsaWduPSdjZW50ZXInIGJnY29sb3I9JyNFN0U3RTcnIGhlaWdodD0nMjInIGNsYXNzPSd0YWJsZVRpdGxlJyA+PFREIHdpZHRoPSIxNSUiIHN0eWxlPSJmb250LXNpemU6MTFwdDsiPuays+WQjTwvVEQ+PFREIHdpZHRoPSIyNSUiIHN0eWxlPSJmb250LXNpemU6MTFwdDsiPuermeWQjTwvVEQ+PFREIHdpZHRoPSIyMCUiIHN0eWxlPSJmb250LXNpemU6MTFwdDsiPuawtOS9jTwvVEQ+PFREIHdpZHRoPSIyMCUiIHN0eWxlPSJmb250LXNpemU6MTFwdDsiPua1gemHjzwvVEQ+PFREIHdpZHRoPSIyMCUiIHN0eWxlPSJmb250LXNpemU6MTFwdDsiPuWQq+aymemHjzwvVEQ+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuS4iemXqOWzoSAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPjI3MC45NTwvdGQ+PHRkPjE1PC90ZD48dGQ+KjAuODMwPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7lsI/mtarlupXkuIrok4TmsLTph488L3RkPjx0ZD4yMzEuMTY8L3RkPjx0ZD4oMTEuOSnkur88L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7lsI/mtarlupUgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD4xMzYuMzc8L3RkPjx0ZD40MzcwPC90ZD48dGQ+KjAuMzM0PC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+5LyK5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7kuJzmub4gICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPjM2My4wMzwvdGQ+PHRkPjUuNzc8L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+5LyK5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7pmYbmtZHlnZ3kuIrok4TmsLTph488L3RkPjx0ZD4zMTQuMTI8L3RkPjx0ZD4oNC42NSnkur88L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+5LyK5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7pmYbmtZHlnZ3kuIrlh7rlupM8L3RkPjx0ZD4tPC90ZD48dGQ+NjwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7kvIrmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPum+memXqOmVhyAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPjE0Ny4zMjwvdGQ+PHRkPjYuMzA8L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+5rSb5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7ljaLmsI8gICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPjU0OS44ODwvdGQ+PHRkPjEuNDQ8L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+5rSb5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7mlYXljr/msLTlupPok4TmsLTph488L3RkPjx0ZD41MTkuNzM8L3RkPjx0ZD4oMy44OCnkur88L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+5rSb5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7mlYXljr/msLTlupPlh7rlupM8L3RkPjx0ZD4tPC90ZD48dGQ+LTwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7mtJvmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPumVv+awtO+8iOS6jO+8iSAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+Mzc3Ljk1PC90ZD48dGQ+My40NzwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7mtJvmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPueZvemprOWvuiAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPjExMi41OTwvdGQ+PHRkPjE0LjM8L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+5LyK5rSb5rKzICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+6buR55+z5YWzICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+MTA0LjU4PC90ZD48dGQ+MTAuODwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7kuLnmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuWxsei3r+WdqiAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPi08L3RkPjx0ZD4tPC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPuaygeaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+5LqU6b6Z5Y+jICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+MTQxLjM3PC90ZD48dGQ+NS42MDwvdGQ+PHRkPi08L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7msoHmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuatpumZnyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+OTguMjwvdGQ+PHRkPjEuNzk8L3RkPjx0ZD4tPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7oirHlm63lj6MgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD45MC43MzwvdGQ+PHRkPjQyMDA8L3RkPjx0ZD4yLjg1PC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7lpLnmsrPmu6kgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD43My4zMzwvdGQ+PHRkPjQyMDA8L3RkPjx0ZD4zLjkxPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7pq5jmnZEgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPjU5LjcyPC90ZD48dGQ+NDE0MDwvdGQ+PHRkPjcuMzc8L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuWtmeWPoyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+NDUuNzI8L3RkPjx0ZD40MTMwPC90ZD48dGQ+NC41ODwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPuWkp+axtuaysyAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuaItOadkeWdnTwvdGQ+PHRkPi08L3RkPjx0ZD4tPC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPuS4nOW5s+a5liAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuS4nOW5s+a5luiAgea5luiThOawtOmHjzwvdGQ+PHRkPjQwLjU2PC90ZD48dGQ+KDMuODYp5Lq/PC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPuWkp+axtuaysyAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuWHuua5lumXuDwvdGQ+PHRkPi08L3RkPjx0ZD4tPC90ZD48dGQ+LTwvdGQ+PC90cj48dHIgYWxpZ249ImNlbnRlciIgYmdjb2xvcj0iI0ZGRkZGRiI+PHRkPum7hOaysyAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+6Im+5bGxICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD4zOS40NDwvdGQ+PHRkPjQwNzA8L3RkPjx0ZD43LjEyPC90ZD48L3RyPjx0ciBhbGlnbj0iY2VudGVyIiBiZ2NvbG9yPSIjRkZGRkZGIj48dGQ+6buE5rKzICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPjx0ZD7ms7rlj6MgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPjI4LjI2PC90ZD48dGQ+NDA1MDwvdGQ+PHRkPjUuOTI8L3RkPjwvdHI+PHRyIGFsaWduPSJjZW50ZXIiIGJnY29sb3I9IiNGRkZGRkYiPjx0ZD7pu4TmsrMgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+PHRkPuWIqea0pSAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD48dGQ+MTEuNTM8L3RkPjx0ZD40MDAwPC90ZD48dGQ+Ny4wNTwvdGQ+PC90cj48L3RhYmxlPjwvdGQ+PC90cj48L3RhYmxlPmRk6SLEnRLOHmIqrYFUEJwjjUKXkaWmUR8wu4QsASYOLBI=',
    '__VIEWSTATEGENERATOR': 'E4DC7756',
    '__EVENTVALIDATION': '/wEdAAMwh7WY8IYhdrMFCrA8OPD09DkLBAR+UXBBGQ1m5cY+HY5Ggl8DGIT46Qo2GBY6Yh54ySi4+4s3+VDKxDcjS9ys207IY1EE9+lI4o+gPt4P7A==',
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
        print('Start time is greater than end time !')
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
                    response_contents_lists.append(single_response_content.contents[0])

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

        Next_response.raise_for_status()
        Next_response.encoding = Next_response.apparent_encoding
        # Get the returned infomation
        Next_response = Next_response.text

        Information_lists = Information_extraction(Next_response)

        Result_excel = Generate_excel(Information_lists)

        Result_save(Save_path,Result_excel,date_list)

        print(f'Date : {date_list} ,data download is complete !')









