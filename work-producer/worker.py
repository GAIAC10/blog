# 一般写在一个APP下面的tasks中 (初始化worker一般在blog/blog的celery.py文件中)

# 消费者

from celery import Celery

# 创建worker
app=Celery('sms-celery',
           broker='redis://:123456@127.0.0.1:6379/2')

# 装饰器必须是自定义app名字.task()
@app.task()
def task_test():
    print('task is running...')

# 在该文件的上一级文件中的terminal中：celery -A worker(work-producer文件的xxx.py) worker --loglevel=info 启动celery进程(简写：celery -A worker worker -l info)


# demo0(可以对比来看)
# tasks.py
from celery import Celery

# 自定义一个work的app
app=Celery('yukang',broker='redis://:123456@127.0.0.1:6379/2')

# 装饰器必须是自定义app名字.task()
@app.task()
def task_test():
    print('task is running...')

# 在该文件的上一级文件中的terminal启动work文件：celery -A tasks(work文件的xxx.py) worker -l info