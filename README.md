##在此项目中，需要配置:  
###(1)cors的配置  
1.INSTALLED_APPS 中添加 corsheaders  
2.MIDDLEWARE 中添加 corsheaders.middleware.CorsMiddleware ,位置尽量靠前，官方建议 ‘django.middleware.common.CommonMiddleware’ 上方  
3.CORS_ORIGIN_ALLOW_ALL  布尔值  如果为True 白名单不启用  
4.CORS_ALLOW_METHODS = (  
                'DELETE',  
                'GET',  
                'OPTIONS',  
                'PATCH',  
                'POST',  
                'PUT',  
                )  
5.CORS_ALLOW_HEADERS = (  
                'accept-encoding',  
                'authorization',  
                'content-type',  
                'dnt',  
                'origin',  
                'user-agent',  
                'x-csrftoken',  
                'x-requested-with',  
            )  
###(2)cache_settings的配置  
CACHES = {  
    "default": {  
            "BACKEND": "django_redis.cache.RedisCache",  
            "LOCATION": "redis://127.0.0.1:6379",  
            "OPTIONS": {  
                "CLIENT_CLASS": "django_redis.client.DefaultClient",  
            }  
        }  
}  
***
##关于一些api接口  
###Users_API  
####事件定义  
1.注册 - 新用户可通过此功能注册为内部论坛的注册用户。每个注册用户可申请一个自己独立的博客空间，只有注册用户方可在自己的博客中发表自己的博客及在博客内容上留言及回复他人的留言。  
2.登陆 - 用户可通过此功能进行用户登陆操作，只有登陆的用户方可执行会员的相关操作-如发布博客及留言功能。  
3.修改个人信息 - 每个注册用户都有 个人描述，个人签名及头像和昵称 可供自定义编写；用户需要进行登陆后，方可使用该功能。  
  
####数据库结构  
![image](https://user-images.githubusercontent.com/72537626/220529218-3daba78d-b758-416d-bab8-9473dca356db.png)  
![image](https://user-images.githubusercontent.com/72537626/220529243-8ffc8cac-d124-450c-8a3c-b3e565a7bfaa.png)  
  
####接口说明  
(1)注册api  
![image](https://user-images.githubusercontent.com/72537626/220527762-6822fd85-5f78-4a13-b74a-e33103dc8525.png)  
响应格式  
![image](https://user-images.githubusercontent.com/72537626/220527887-d09c6e3f-1dc3-4df4-b2e7-787dd3725345.png)  
异常码  
![image](https://user-images.githubusercontent.com/72537626/220527943-12fcf23f-392c-47d4-a7f7-48a3e02021aa.png)  
  
(2)获取用户数据api  
![image](https://user-images.githubusercontent.com/72537626/220528091-031d9f5b-bca7-4c25-aa4d-e7d8988cf5f0.png)  
响应格式  
![image](https://user-images.githubusercontent.com/72537626/220528125-f0e6fe2f-65fd-43ae-a97b-fc1df776c193.png)  
异常码  
![image](https://user-images.githubusercontent.com/72537626/220528191-76899404-3aed-4dd7-bafa-cbf00cb230e9.png)  
  
(3)修改用户个人信息api  
![image](https://user-images.githubusercontent.com/72537626/220528315-4675f80b-bf97-4648-83f6-f956efa21917.png)  
请求格式  
![image](https://user-images.githubusercontent.com/72537626/220528346-ebee019c-a7fd-43da-bb67-45b9d3641ba6.png)  
响应格式  
![image](https://user-images.githubusercontent.com/72537626/220528368-6179b6dc-5e94-44f8-aea1-5fe2d67cf0b7.png)  
异常码  
![image](https://user-images.githubusercontent.com/72537626/220528404-c8fea901-5a57-491a-8777-f1ff73d8fa43.png)  
  
(4)上传头像api  
![image](https://user-images.githubusercontent.com/72537626/220528536-0a2e8a48-5f58-4d47-b8b8-7d3e575e0849.png)  
响应格式  
![image](https://user-images.githubusercontent.com/72537626/220528593-7b468be9-b5f1-4530-abb0-ef6e29ad4978.png)  
  
(5)获取token  
![image](https://user-images.githubusercontent.com/72537626/220528648-ca76804e-8f6f-4064-b066-748da6bdbbbf.png)  
响应格式  
![image](https://user-images.githubusercontent.com/72537626/220528716-e1ba1210-bca9-46c3-8ab9-68da9fd2d19e.png)  
异常码  
![image](https://user-images.githubusercontent.com/72537626/220528765-7e413fd0-2b9e-4500-a384-07011cc753c7.png)  
  
###Messages_API  
####事件定义:  
1.发表博客留言 - 登录状态下，用户可以在任何人的博客内容详情页进行留言  
2.回复博客留言 - 登录状态下， 任何用户可以回复任何用户的留言  
  
####数据库结构  
![image](https://user-images.githubusercontent.com/72537626/220532195-3234f1dd-d0bd-43a9-891f-167da29c0806.png)  
  
####接口说明  
(1)发表博客留言  
![image](https://user-images.githubusercontent.com/72537626/220532343-ebf91272-7395-4468-a024-d6b4d9d4cc37.png)  
响应格式  
![image](https://user-images.githubusercontent.com/72537626/220532396-75cfaf73-5bba-4f42-b71e-c31b2423aac0.png)  
异常码  
![image](https://user-images.githubusercontent.com/72537626/220532455-1c5c4aca-9e25-4acf-95de-d5a15c0e117f.png)  
  
###Topic_API  
####事件定义  
1.获取博客列表 - 获取用户的博客列表，博客分为 技术和非技术两大类别；权限分为个人和公开。 其中个人博客只有在博主登录状态下才能获取  
2.发表博客 - 只有博主在登录状态下才能执行发表博客操作  
  
####数据库结构  
![image](https://user-images.githubusercontent.com/72537626/220531393-16a3958d-d19d-421f-a68a-00ecb8fb9f47.png)  
![image](https://user-images.githubusercontent.com/72537626/220531405-fce08068-6f7c-4266-9d29-dcb52acbab73.png)  
  
####接口说明  
(1)发表博客api  
![image](https://user-images.githubusercontent.com/72537626/220530835-caacaf11-283d-4668-a235-5c6407b04bce.png)  
请求格式  
![image](https://user-images.githubusercontent.com/72537626/220530890-15fbe8af-e024-46c4-84b8-a86d38ed1cde.png)  
响应格式  
![image](https://user-images.githubusercontent.com/72537626/220530958-38c0653f-af78-42c2-ae97-3ed9b9238c70.png)  
异常码  
![image](https://user-images.githubusercontent.com/72537626/220531004-767b45fd-d803-4fa9-90b7-667f649798db.png)  
  
(2)获取用户博客列表api  
![image](https://user-images.githubusercontent.com/72537626/220529659-e08b0365-4b29-49bc-b806-4223428ca2b2.png)  
响应格式   
![image](https://user-images.githubusercontent.com/72537626/220529712-5ded9bb3-6738-4562-ba43-815bc96b033d.png)  
异常码  
![image](https://user-images.githubusercontent.com/72537626/220529740-f1477244-b787-47b3-a6c1-5bcb8a3182cf.png)  
  
(3)获取用户具体博客内容api  
![image](https://user-images.githubusercontent.com/72537626/220529790-f7dcac18-aaa5-4ade-969f-620ef07dbe63.png)  
响应格式  
![image](https://user-images.githubusercontent.com/72537626/220530122-62568b03-f410-466c-b0fe-4ef9ba0c5a44.png)  
响应实例  
![image](https://user-images.githubusercontent.com/72537626/220530283-a8130ff8-a936-48db-b4bb-f28dead10c5b.png)  
![image](https://user-images.githubusercontent.com/72537626/220530318-157fa3ce-715c-46d6-9f1b-3ca878f1aaf4.png)  
异常码  
![image](https://user-images.githubusercontent.com/72537626/220530350-df96e6be-bda7-4db9-8a22-521790ff19e1.png)  
   
(4)删除博客api  
![image](https://user-images.githubusercontent.com/72537626/220530400-2a2b4245-69a6-48c3-9a4e-f731648b7b20.png)  
响应格式  
![image](https://user-images.githubusercontent.com/72537626/220530423-973dd49b-6dcd-4b40-b36c-0b67abe650a3.png)  
异常码   
![image](https://user-images.githubusercontent.com/72537626/220530446-38378dba-b4b8-4239-87f8-fc09ae33647a.png)  












