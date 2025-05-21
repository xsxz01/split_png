import certifi
import requests
import os
from urllib.parse import urlencode

http_url = "https://w.eydata.net"
API_单码用户登录 = '/8517BD8A7F520F1A'
API_获取用户到期时间 = '/5ABABE0AFD3C510B'

def http_post(url,data):  
    try:
        headers={
            "Content-Type":"application/x-www-form-urlencoded"
        }
        if not url.startswith('/'):
            url = '/' + url
        url_encoded = urlencode([(key, value) for key, value in data.items()])
        r = requests.post(http_url+url,data=url_encoded,headers=headers,timeout=30)
        if r.status_code==200:
            result=str(r.text)
        else:
            result="遇到错误，请检查网络重试"    
        return result
    except Exception as e:
        print(e)
        return "遇到错误，请检查网络重试"

def login(SingleCode: str, Ver: str, Mac: str):
    data = {
    # 单码卡密
        'SingleCode':SingleCode,
    # 版本号
        'Ver':Ver,
    # 机器码
        'Mac':Mac,
    }
    ret = http_post(API_单码用户登录,data)
    print(ret)
    if len(ret)==32 :
        print('登录成功，状态码：' + ret)
    else:
        print('登录失败，错误码：' +ret)

def get_expire_time(UserName: str):
    data = {
        'UserName': UserName,
    }
    ret = http_post(API_获取用户到期时间,data)
    if len(ret)==10 :
        print('获取到期时间成功，到期时间：' + ret)
    else:
        print('获取到期时间失败，错误码：' +ret)