from django.db import models
from usersss.models import UserProfile

# Create your models here.
# 关于简介的处理：
# 1.后端给前端文章全部内容，前端自己截取（X）
# 2.后端从数据库中获取全部文章内容，后端截取好后响应给前端（X）
# 3.数据库中新建一个字段[简介]，后端只取简介字段内容

class Topic(models.Model):
    title=models.CharField(max_length=50,verbose_name='文章标题')
    category=models.CharField(max_length=20,verbose_name='文章分类')
    limit=models.CharField(max_length=20,verbose_name='文章权限')
    introduce=models.CharField(max_length=90,verbose_name='文章简介')
    content=models.TextField(verbose_name='文章内容')
    create_time=models.DateTimeField(auto_now_add=True)
    update_time=models.DateTimeField(auto_now=True)
    # on_delete=models.CASCADE表示auther被删除的话，Topic也会被删
    # obj
    author=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
