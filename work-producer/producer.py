# 一般写在views中

# 没有backend属性时，不返回数据
from worker import task_test
task_test.delay()

# 有backend属性时，返回s的结果
from .worker_backend import task_test
task_test.delay(10,100)


# demo0(可以对比来看)
# producer.py
# 没有backend属性时，不返回数据
# from tasks import task_test
# task_test.delay()

# 有backend属性时，返回s的结果
# from tasks_result import task_test
# s=task_test.delay(10,100)
