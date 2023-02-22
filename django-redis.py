# 法一
from django.core.cache import cache
d=['a','b','c']
cache.set('test1',d,120)
print(cache.get('test1'))

# 法二：
from django_redis import get_redis_connection
r=get_redis_connection()
r.set('test1',d,120)
print(r.get('test1'))


# 缓存方案

# 一、cache_page(过期时间[s])
# 缺点：
# 1.不能区分博主和访客的身份
# 2.删除成本高(新旧数据不一致)
# 用法：
# 放到视图函数的上面（将视图函数返回的数据放到配置的redis）
# cache_page()是函数类装饰器，需要@method_decorator(cache_page())转化为方法类装饰器

# 二、cache.set/get
# 缺点：
# 在每一次查询是都需要cache.set/get,代码成本高

# 三、自己写装饰器



