"""project3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.views.static import serve
from django.conf import settings
from RedemptionII.views import Department, User, PrettyNumber, Admin, Account, Task, Order, Chart, Upload, Team

urlpatterns = [

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),

    # path('admin/', admin.site.urls),

    # ######## 部门管理 #########

    # 部门列表
    path('depart/list/', Department.depart_list),

    # 添加部门
    path('depart/add/', Department.depart_add),

    # 删除部门
    path('depart/delete/', Department.depart_delete),

    # 编辑部门
    # <int:nid> 相当于 /depart/1/edit(1可以是其它整数)
    path('depart/<int:nid>/edit/', Department.depart_edit),

    # 上传文件
    path('depart/multi/', Department.depart_multi),

    # ####### 用户管理 ##########

    # 用户列表
    path('user/list/', User.user_list),

    # 添加用户
    path('user/add/', User.user_add),

    # 添加用户(ModelForm方式)
    path('user/model/form/add/', User.user_model_form_add),

    # 编辑用户(ModelForm方式)
    path('user/<int:nid>/edit/', User.user_edit),

    # 删除用户(ModelForm方式)
    path('user/<int:nid>/delete/', User.user_delete),

    # #########靓号管理##########
    # 靓号列表
    path('pretty/list/', PrettyNumber.pretty_list),

    # 添加靓号
    path('pretty/add/', PrettyNumber.pretty_add),

    # 编辑靓号
    path('pretty/<int:nid>/edit/', PrettyNumber.pretty_edit),

    # 删除靓号
    path('pretty/<int:nid>/delete/', PrettyNumber.pretty_delete),

    # #########管理员专属##########
    # 管理员列表
    path('admin/list/', Admin.admin_list),

    # 新建管理员
    path('admin/add/', Admin.admin_add),

    # 编辑管理员
    path('admin/<int:nid>/edit/', Admin.admin_edit),

    # 删除管理员
    path('admin/<int:nid>/delete/', Admin.admin_delete),

    # 重置密码
    path('admin/<int:nid>/reset/', Admin.admin_reset),

    # #########用户登录##########
    # 登录
    path('login/', Account.login),

    # 注销登录
    path('logout/', Account.logout),

    # 图片验证码部分
    path('image/code/', Account.image_code),

    # #########任务管理#########
    path('task/list/', Task.task_list),

    # 利用 Ajax 发送请求
    path('task/add/', Task.task_add),

    # #########订单管理#########
    path('order/list/', Order.order_list),

    # 接收用户订单
    path('order/add/', Order.order_add),

    # 删除用户订单
    path('order/delete/', Order.order_delete),

    # 显示用户订单细节(用于编辑)
    path('order/detail/', Order.order_detail),

    # 编辑用户订单
    path('order/edit/', Order.order_edit),

    # #########制作分析图表#########
    path('chart/list/', Chart.chart_list),

    # 制作柱状图
    path('chart/bar/', Chart.chart_bar),

    # 制作饼状图
    path('chart/pie/', Chart.chart_pie),

    # 制作折线图
    path('chart/line/', Chart.chart_line),

    # highChart 示例
    path('chart/hightcharts/', Chart.hightcharts),

    # #########制作分析图表#########
    path('upload/list/', Upload.upload_list),

    # form 方式上传文件
    path('upload/form/', Upload.upload_form),

    # ModelForm 方式上传文件
    path('upload/model/form/', Upload.upload_model_form),

    # 团队列表
    path('team/list/', Team.team_list),

    # 新建团队
    path('team/add/', Team.team_add),
]
