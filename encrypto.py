import rsa
import json
import time
import http.client

pub_key = """
-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAh8LJRYHCre92mpvfGk+Z89UixuBOHmxTDKjNn1fY1yfpATMAxUGG
liwEuNxChiyVGZwJg2WqVqN8swH6EKb46AGLqDryhHjs4Cx5cvwMtVqnTnI+ae7x
RPI4a5zpn5ffosk09bkUMBRCy9YuIFfzts8gIsH73ZyQ/KDCd1uGhmTymXjufBAr
sOW4JbHA7cXPBXDI5LTcMSVjhVTgXqCcYOwjrAeAVXVTrn8+NW+ttJDxC2Vk3fvT
T4J+NzclkXhOhRGY9RpJ+wxfIdOlVETJwbdsI1pLqH4dmoNkPHUn/rg0U8D+rkQ/
X/oT96Yf1SVaBZdaDCVgao7dS1Nz9OVwEwIDAQAB
-----END RSA PUBLIC KEY-----
"""

pub_key = rsa.PublicKey.load_pkcs1(pub_key)

info = dict()

dead_line = input("请输入截止日期(YYYY-MM-DD)：").strip()
ID = input("请输入账号：")
passwd = input("请输入密码：")
de = int(input("选择出租的客户端 1.PC 2.手机："))

while True:
    try:
        time.strptime(dead_line, "%Y-%m-%d")
        break
    except:
        print("日期格式输入错误，重新输入，示例：2020-01-31")
        dead_line = input("请输入截止日期(YYYY-MM-DD)：").strip()
        continue

info["expire"] = dead_line
info["ID"] = ID
info["passwd"] = passwd
info["device"] = de - 1

with open("term.auth", "wb") as f:
    f.write(rsa.encrypt(json.dumps(info).encode(),pub_key=pub_key))

print((json.loads(json.dumps(info))))

print("已成功生成授权文件: term.auth")