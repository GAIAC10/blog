from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
import json
from .models import UserProfile
import hashlib
from django.utils.decorators import method_decorator
from tools.logging_dec import logging_check
import random
# redis和django的caches
import django_redis
from django.core.cache import cache
from tools.sms import YunTongXin
from django.conf import settings
from .tasks import send_sms_c

# 在F12之后，Network中的Response中可以查看自定义的状态码
# 异常码自定义：
# 10100~10199
# 每个码代表的情况自己定

# Create your views here.
class UserViews(View):
    # 用户个人主页（用于返回用户数据）
    def get(self,request,username=None):
        # 令username=None是因为不让v1/user进入，要让v1/user/yukang进入
        if username:
            # /v1/user/yukang
            try:
                user=UserProfile.objects.get(username=username)
            except Exception as e:
                # 因为用户名是主键，不可能查多了，而是用户名错误
                result={'code':10102,'error':'用户名不存在'}
                return JsonResponse(result)
            # 头像：str（）是直接返回数据库中的数据
            result={'code':200,'username':username,'data':{'info':user.info,'sign':user.sign,'nickname':user.nickname,'avatar':str(user.avatar)}}
            return JsonResponse(result)
        else:
            # /v1/user
            pass

    # 注册
    # 注册所有的信息都传到该函数了
    def post(self,request):
        # 前端发送数据的类型是contentType:'application/json',如果用request.POST则取不到数据

        # 想要取到json数据:request.body
        json_str=request.body
        json_obj=json.loads(json_str)
        username=json_obj['username']
        email=json_obj['email']
        password_1=json_obj['password_1']
        password_2=json_obj['password_2']
        phone=json_obj['phone']
        sms_num=json_obj['sms_num']

        # 参数基本检查

        # 两次密码是否正确
        if password_1!=password_2:
            result={'code':10100,'error':'The password is not same'}
            return JsonResponse(result)

        # 验证码比对
        old_code=cache.get('sms_%s'%(phone))
        if not old_code:
            result={'code':'10110','error':'The code is wrong'}
            return JsonResponse(result)
        if int(sms_num)!=old_code:
            result={'code':'10111','error':'The code is wrong'}
            return JsonResponse(result)

        # 用户名是否可用
        # get返回的是value(需要try一下)，filter返回的是编号（Q...set）（不用try）
        old_users=UserProfile.objects.filter(username=username)
        if old_users:
            result={'code':10101,'error':'The username is already existed'}
            return JsonResponse(result)

        # 正确时
        # 向UserProfile插入数据（密码md5存储）
        p_m=hashlib.md5()
        # 将字符串转化为字节串
        p_m.update(password_1.encode())
        UserProfile.objects.create(username=username,nickname=username,password=p_m.hexdigest(),email=email,phone=phone)
        result={'code':200,'username':username,'data':{}}
        return JsonResponse(result)

    # 更新个人数据（昵称，个人签名，个人描述）
    @method_decorator(logging_check)
    def put(self,request,username=None):
        json_str=request.body
        json_obj=json.loads(json_str)
        user=request.myuser
        # try:
        #     user = UserProfile.objects.get(username=username)
        # except Exception as e:
        #     result = {'code': 10105, 'error': 'The username is error'}
        #     return JsonResponse(result)
        user.sign=json_obj['sign']
        user.info=json_obj['info']
        user.nickname=json_obj['nickname']
        user.save()
        return JsonResponse({'code':200})



# 头像的更改
@logging_check
def users_views(request,username):
    if request.method!='POST':
        result={'code':10103,'error':'Please use POST'}
        return JsonResponse(result)
    user=request.myuser
    # 因为装饰器中有token的user，这里还有传参传进来的username，更相信token里面的user
    # try:
    #     user=UserProfile.objects.get(username=username)
    # except Exception as e:
    #     result={'code':10104,'error':'The username is error'}
    #     return JsonResponse(result)

    # 一查二改三更新
    avatar=request.FILES['avatar']
    user.avatar=avatar
    user.save()
    return JsonResponse({'code':200})

# 密码修改
@logging_check
def change_password(request,username):
    json_str = request.body
    json_obj = json.loads(json_str)
    user = request.myuser
    mysql_username=user.username
    mysql_password=user.password
    old_password=json_obj['old_password']
    password_1=json_obj['password_1']
    password_2=json_obj['password_2']

    # 用户名校验
    if username != mysql_username:
        result = {'code': 19999, 'error': 'The username is wrong'}
        return JsonResponse(result)

    # 校验密码
    p_m=hashlib.md5()
    p_m.update(old_password.encode())
    if p_m.hexdigest()!=user.password:
        result={'code':19998,'error':'Password mistake'}
        return JsonResponse(result)

    # 重复密码校验
    if password_1!=password_2:
        result={'code':19997,'error':'You two entered passwords do not match'}
        return JsonResponse(result)

    n_p=hashlib.md5()
    n_p.update(password_1.encode())
    user.password = n_p.hexdigest()
    user.save()
    return JsonResponse({'code': 200})


# 因为class中的def（方法）有（self参数），而在外面的def（函数）没有（self参数），则在使用装饰器的时候，参数个数不同，则不能给功能相同的def使用
# 但是django提供了一个装饰器 mothod_decorator（装饰我们的装饰器），可以将函数装饰器转换为方法装饰器
# 在有mothod_decorator之后，就只需要自己写一个函数装饰器（外面），方法装饰器只需要@mothod_decorator（函数装饰器）既可

# 短信的发送
def sms_view(request):
    if request.method!='POST':
        result={'code':10108,'error':'Please use POST'}
        return JsonResponse(result)
    json_str=request.body
    json_obj=json.loads(json_str)
    phone=json_obj['phone']
    # 生成随机码
    code=random.randint(1000,9999)
    print('phone',phone,'code',code)
    # 存储随机码（之前是redis，现在是django_redis（将redis和django的缓存结合））
    cache_key='sms_%s'%(phone)
    # 检查是否已经有发送的且没有过期的验证码
    old_code=cache.get(cache_key)
    if old_code:
        result={'code':10111,'error':'The code is already existed'}
        return JsonResponse(result)

    cache.set(cache_key,code,60)
    # 发送随机码->短信
    # send_sms(phone,code)

    # 发送短信时运用 生产者消费者模型（celery版）
    # 运行worker时，在总的项目下:celery -A blog worker -l info
    send_sms_c.delay(phone,code)

    return JsonResponse({'code':200})

# 短信发送
def send_sms(phone,code):
    config={
        'accountSid':settings.ACCOUNTSID,
        'accountToken':settings.ACCOUNTTOKEN,
        'appId':settings.APPID,
        'templateId':settings.TEMPLATEID
    }
    yun=YunTongXin(**config)
    res=yun.run(phone,code)
    return res
