from celery import Celery

# 创建worker
app=Celery('sms-celery',
           broker='redis://:123456@127.0.0.1:6379/2',
           backend='redis://:123456@127.0.0.1:6379/3')

# 装饰器必须是自定义app名字.task()
@app.task()
def task_test(a,b):
    print('task is running...')
    return a+b

# 在该文件的上一级文件中的terminal启动work文件：celery -A worker_backend(work文件的xxx.py) worker -l info


# demo0(可以对比来看)
# tasks_result.py
from celery import Celery

# 自定义一个work的app
app=Celery('yukang_result',broker='redis://:123456@127.0.0.1:6379/2',
           backend='redis://:123456@127.0.0.1:6379/3')

# 装饰器必须是自定义app名字.task()
@ app.task()
def task_test(a,b):
    print('task is running...')
    return a+b

# 在该文件的上一级文件中的terminal启动work文件：celery -A tasks_result(work文件的xxx.py) worker -l info