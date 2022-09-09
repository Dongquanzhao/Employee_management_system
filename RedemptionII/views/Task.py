import json

from django import forms
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from RedemptionII import models
from RedemptionII.utils.bootstrap import BootstrapModelForm
from RedemptionII.utils.pagination import Pagination


class TaskModelForm(BootstrapModelForm):
    class Meta:
        model = models.Task
        fields = '__all__'
        widgets = {
            'detail': forms.TextInput,
            # 'detail': forms.Textarea,
        }


def task_list(request):

    """任务列表"""

    # 去数据库获取所有任务
    queryset = models.Task.objects.all().order_by('-id')
    page_object = Pagination(request, queryset)
    form = TaskModelForm()
    context = {
        'form': form,
        'queryset': page_object.page_queryset,  # 分完页的数据
        'page_string': page_object.html(),         # 生成的页码
    }
    return render(request, 'task_list.html', context)


@csrf_exempt
def task_add(request):

    """添加任务"""

    # 用户发过来的数据由 ModelForm 进行校验
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {'status': True}
        return HttpResponse(json.dumps(data_dict))

    data_dict = {'status': False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))













