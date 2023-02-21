import http.client
import time
import rsa
from CQNU_helper import LoginIntoCqnu
import json
import sys

private_key = """
为保证授权文件不被破解，私钥不公开
"""

def net_test():
    try:
        http.client.HTTPConnection("baidu.com").request("GET", "/")
        return True
    except:
        return False

def get_time():
    conn = http.client.HTTPConnection("10.0.254.125:801")
    conn.request("GET", "/")
    r = conn.getresponse()
    ts =  r.getheader('date')
    ltime = time.strptime(ts[5:25], "%d %b %Y %H:%M:%S")
    ttime = time.localtime(time.mktime(ltime)+8*60*60)
    return ttime

if __name__ == "__main__":

    pri_key = rsa.PrivateKey.load_pkcs1(private_key, format="PEM")

    print("加载授权文件(term.auth)...")
    try:
        with open("term.auth", "rb") as f:
            term = f.read()
        print("✓ 加载成功")
    except:
        print("X 加载失败 [error_code: 00]")
        print("请保证授权文件在本程序所在目录")
        sys.exit()

    de_term = rsa.decrypt(crypto=term, priv_key=pri_key)

    info = json.loads(de_term.decode())

    today = get_time()

    print("认证授权信息...")

    expire_time = time.strptime(info["expire"], "%Y-%m-%d")

    print(f"授权文件到期时间：{expire_time.tm_year:4}-{expire_time.tm_mon:02}-{expire_time.tm_mday:02}")
    print(f"当前日期：{today.tm_year:4}-{today.tm_mon:02}-{today.tm_mday:02}")

    if expire_time < today:
        print("X 已超出授权时间，请联系出租者重新生成授权文件 [error_code: 10]")
        sys.exit()

    print("✓ 授权检测完成，正在登陆...")

    logger = LoginIntoCqnu.LoginIntoCqnu(info["ID"], info["passwd"],device=info["device"])

    r = logger.login()
    
    print("测试网络连通性...")

    time.sleep(2)

    while not net_test():
        print("X 连通网络失败，重新登陆中... [error_code: 20]")
        r = logger.login()
    
    print("✓ 连接正常，登陆成功!!!")

    input("回车以关闭窗口")