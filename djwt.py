import jwt
import time

# {'username': 'yukang'}是明文, '123456'是加密的key, algorithm='HS256'是算法名
# exp表示的是过期时间
s=jwt.encode({'username': 'yukang','exp':time.time()+3}, '123456',algorithm='HS256')

# print(jwt.decode(s,'123456'))
# {'username': 'yukang', 'exp': 1627099340.2975252}


# print(s)
# b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Inl1a2FuZyJ9.b4ndWef5tVoDNuyc-LicAXQTkqTQZtdAMAYmlyCjo9w'

# 正确则返回明文，错误则报错
# print(jwt.decode(s,'123456'))
# {'username': 'yukang'}

# print(jwt.decode(s,'12345'))
# jwt.exceptions.InvalidSignatureError: Signature verification failed
