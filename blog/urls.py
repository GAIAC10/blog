"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
# 用于连接media
from django.conf import settings
from django.conf.urls.static import static
from usersss import views as user_views
from dtaken import views as dtoken_views

urlpatterns = [
    # path函数在匹配网址的时候最开始不能有斜杠
    path('admin/', admin.site.urls),
    path('test_cors',views.test_cors),
    path('v1/users',user_views.UserViews.as_view()),
    # 下面在user的最后是有/的
    path('v1/users/',include('usersss.urls')),
    path('v1/tokens',dtoken_views.tokens),
    path('v1/topics/',include('topic.urls')),
    path('v1/messages/',include('message.urls'))

]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)