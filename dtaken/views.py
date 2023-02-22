from django.http import JsonResponse
from django.shortcuts import render
import json
from usersss.models import UserProfile
import hashlib
from django.conf import settings
import time
import jwt

# Create your views here.

# 异常码 10200~10299

# 登陆
def tokens(request):
    if request.method!='POST':
        result={'code':10200,'error':'Please use POST'}
        return JsonResponse(result)
    json_str=request.body
    json_obj=json.loads(json_str)
    username=json_obj['username']
    password=json_obj['password']
    # 校验用户名和密码
    try:
        user=UserProfile.objects.get(username=username)
    except Exception as e:
        result={'code':10201,'error':'The username or password is wrong'}
        return JsonResponse(result)
    p_m=hashlib.md5()
    p_m.update(password.encode())
    if p_m.hexdigest()!=user.password:
        result={'code':10202,'error':'The username or password is wrong'}
        return JsonResponse(result)
    # 记录会话状态
    token=make_token(username)
    result={'code':200,'username':username,'data':{'token':token.decode()}}
    return JsonResponse(result)

# 用于生成token
def make_token(username,expire=3600*24):
    # 需要到settings中去配置key
    key=settings.JWT_TOKEN_KEY
    new_t=time.time()
    payload_data={'username':username,'exp':new_t+expire}
    # 生成的jwt是字节串
    return jwt.encode(payload_data,key,algorithm='HS256')

