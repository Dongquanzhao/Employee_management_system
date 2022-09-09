import os

from django import forms
from django.conf import settings
from django.shortcuts import render, HttpResponse

from RedemptionII import models
from RedemptionII.utils.bootstrap import BootstrapForm, BootstrapModelForm


def upload_list(request):
    """上传文件"""

    return render(request, 'upload_list.html')


class UpForm(BootstrapForm):
    bootstrap_exclude_fields = ['img']
    name = forms.CharField(label='姓名')
    age = forms.IntegerField(label='年龄')
    img = forms.FileField(label='头像')


def upload_form(request):
    """form 方式批量上传数据"""

    title = "Form上传"
    if request.method == 'GET':
        form = UpForm()
        return render(request, 'upload_form.html', {'form': form, 'title': title})

    form = UpForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 读取文件内容，写入到文件夹中并获取文件的路径
        image_object = form.cleaned_data.get('img')
        media_path = os.path.join('media', image_object.name)
        f = open(media_path, mode='wb')
        for chunk in image_object.chunks():
            f.write(chunk)
        f.close()

        # 将图片文件路径写入到数据库
        models.BestEmployee.objects.create(
            name=form.cleaned_data['name'],
            age=form.cleaned_data['age'],
            img=media_path
        )
        return HttpResponse('...')
    return render(request, 'upload_form.html', {'form': form, 'title': title})


class UpModelForm(BootstrapModelForm):
    bootstrap_exclude_fields = ['img']

    class Meta:
        model = models.BestTeam
        fields = '__all__'


def upload_model_form(request):
    """以 ModelForm 方式上传数据"""

    title = "ModelForm 上传文件"
    if request.method == 'GET':
        form = UpModelForm()
        return render(request, 'upload_form.html', {'form': form, 'title': title})

    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return HttpResponse('成功啦')
    return render(request, 'upload_form.html', {'form': form, 'title': title})
