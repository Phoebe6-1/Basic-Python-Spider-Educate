import re

# 验证合法邮箱
email_pattern=r'^[\w\.]+@[\w\.]+\.\w+$'
def judge(email):
    return re.fullmatch(email_pattern,email) is not None

print(judge('user@example.com'))
print(judge('12345678@qq.com'))
print(judge('user@.com'))
print(judge('user@example_com'))


# 手机号提取
text = "联系方式：13812345678，备用：+8613912345678"
pattern = r'.*?(1[3-9]\d{9})'
phones = re.findall(pattern, text)
print(phones)


# 检查密码强度是否规范(要求至少包含一个大写，小写字母及数字，且长度至少为8位)
pattern=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$'
password=['Pass12345','cyt031616','Phoebe6']
for item in password:
    if re.match(pattern,item):
        print(f"{item} 是规范的")
    else:
        print(f"{item} 不规范")

