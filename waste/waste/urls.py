"""waste URL Configuration

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
from django.urls import path, re_path
from wasteSearch.views import account, about, wasteInfo, userInfo,wasteAdd,wasteManage
from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import staticfiles

urlpatterns = [

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),

    # path('admin/', admin.site.urls),
    path('index/', wasteInfo.index),
    
    path('details/<str:name>/', wasteInfo.details),
    path('compare/<str:name>/<str:comparename>/', wasteInfo.compare),

    path('search/label/', wasteInfo.search_label),
    path('search/modelchoice/', wasteInfo.search_modelchoice),
    path('search/<str:modelname>/', wasteInfo.search_model),

    path('create/',  wasteInfo.create),

    # path('ajax/getLabels/', wasteInfo.getLabels, name='getLabels'),
    # 新增污染物


    # 用户登入登出
    path('login/', account.login),
    path('logout/', account.logout),
    path('image/code/', account.image_code),

    # 用户管理
    path('user/list/', userInfo.userList),
    path('user/add/', userInfo.userAdd),
    path('user/<int:nid>/edit/', userInfo.userEdit),
    path('user/<int:nid>/delete/', userInfo.userDelete),
    path('user/<int:nid>/reset/', userInfo.userReset),

    # 废物数据管理页面
    path('waste/list/', wasteManage.wasteList),
    path('waste/<int:nid>/edit/', wasteManage.wasteEdit),
    path('waste/add/', wasteManage.wasteAdd),
    path('waste/<int:nid>/delete/', wasteManage.wasteDelete),

    # 帮助关于界面
    path('about/', about.about),
    path('help/', about.help),


    # 指纹特征信息
    path('finger/feature/', about.fingerFeature),



]


urlpatterns += staticfiles_urlpatterns()
