from django.shortcuts import render, redirect
from django import forms
from django.core.exceptions import ValidationError

from RedemptionII import models
from RedemptionII.utils.pagination import Pagination
from RedemptionII.utils.bootstrap import BootstrapModelForm
from RedemptionII.utils.Encrypt import md5


def admin_list(request):

    """管理员列表"""

    # # 检查用户是否已经登录，若登录则继续向下走；否则返回登录页面
    # # 用户发来请求，获取cookie随机字符串，拿着随机字符串看看session中有没有
    # info = request.session.get('info')
    # if not info:
    #     return redirect('/login/')

    # 构造搜索条件
    data_dict = {}
    search_data = request.GET.get('q')
    if search_data:
        data_dict['mobile__contains'] = search_data

    # 根据搜索条件去数据库获取
    queryset = models.Admin.objects.filter(**data_dict)

    # 分页
    page_object = Pagination(request, queryset)

    context = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html(),
        'search_data': search_data,
    }
    return render(request, 'admin_list.html', context)


class AdminModelForm(BootstrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True),
    )

    class Meta:
        model = models.Admin
        fields = ["username", 'password', "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm = md5(self.cleaned_data.get('confirm_password'))
        if confirm != pwd:
            raise ValidationError("抱歉，密码不一致！")
        return confirm


class AdminEditModelForm(BootstrapModelForm):
    class Meta:
        model = models.Admin
        fields = ['username']


class AdminResetModelForm(BootstrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True),
    )

    class Meta:
        model = models.Admin
        fields = ['password', 'confirm_password']
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        md5_pwd = md5(pwd)

        # 去数据库校验当前密码和新输入的密码是否一致
        exists = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exists:
            raise ValidationError('修改后的密码不能与之前的密码一致!!!')

        return md5_pwd

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm = md5(self.cleaned_data.get('confirm_password'))
        if confirm != pwd:
            raise ValidationError("抱歉，密码不一致！")
        return confirm


def admin_add(request):

    """添加管理员"""

    title = "新建管理员"

    if request.method == 'GET':
        form = AdminModelForm()
        return render(request, 'change.html', {'form': form, "title": "添加管理员"})

    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'change.html', {'form': form, "title": "添加管理员"})


def admin_edit(request, nid):

    """编辑管理员"""

    # 若存在，则是一个对象。否则为 null
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request, 'error.html', {'msg': '抱歉，数据不存在哟！！'})

    title = '编辑管理员'

    if request.method == 'GET':
        form = AdminEditModelForm(instance=row_object)
        return render(request, 'change.html', {'form': form, 'title': title})

    form = AdminEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'change.html', {'form': form, 'title': title})


def admin_delete(request, nid):

    """删除管理员"""

    models.Admin.objects.filter(id=nid).delete()
    return redirect('/admin/list/')


def admin_reset(request, nid):

    # 若存在，则是一个对象。否则为 null
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect('/admin/list/')

    title = '重置密码 - {}'.format(row_object.username)

    if request.method == 'GET':
        form = AdminResetModelForm()
        return render(request, 'change.html', {'form': form, 'title': title})

    form = AdminResetModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'change.html', {'form': form, 'title': title})


























