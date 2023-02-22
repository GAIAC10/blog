# 关于worker的配置
from celery import Celery
from django.conf import settings
import os

# celery在一个django项目里面可以有多个，区别时需要自定义名字
os.environ.setdefault('DJANGO_SETTINGS_MODULE','blog.settings')

# 新建worker
# app=Celery('blog')

# app=Celery('blog',broker='redis://:123456@127.0.0.1:6379/2')

# app.conf.update(BROKER_URL(官方要求的名字，还有其他的，去文档上查)='redis://:123456@127.0.0.1:6379/1')
app = Celery('blog')
app.conf.update(broker_url='redis://:123456@127.0.0.1:6379/2')

# 自动发现worker函数（去注册的app下面找有没有worker函数）
app.autodiscover_tasks(settings.INSTALLED_APPS)