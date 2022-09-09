import random
from datetime import datetime

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from RedemptionII import models
from RedemptionII.utils.bootstrap import BootstrapModelForm
from RedemptionII.utils.pagination import Pagination


class OrderModelForm(BootstrapModelForm):
    class Meta:
        model = models.Order
        # fields = '__all__'
        exclude = ['oid', 'admin']


def order_list(request):

    queryset = models.Order.objects.all().order_by('-id')
    page_object = Pagination(request, queryset)
    form = OrderModelForm()

    context = {
        'form': form,
        'queryset': page_object.page_queryset,  # 分完页的数据
        'page_string': page_object.html(),  # 生成的页码
    }

    return render(request, 'order_list.html', context)


@csrf_exempt
def order_add(request):

    """新建订单(Ajax请求)"""

    form = OrderModelForm(data=request.POST)
    if form.is_valid():

        # 自动生成特殊的 oid
        form.instance.oid = datetime.now().strftime('%Y%m%d%H%MS') + str(random.randint(10000, 99999))

        # 将订单的管理员设置为当前登录的管理员的 ID
        form.instance.admin_id = request.session['info']['id']

        form.save()
        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'error': form.errors})


def order_delete(request):

    """删除订单"""

    uid = request.GET.get('uid')
    exists = models.Order.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({'status': False, 'error': '抱歉！数据不存在'})

    models.Order.objects.filter(id=uid).delete()
    return JsonResponse({'status': True})


def order_detail(request):

    """根据 ID 获取订单详细"""

    uid = request.GET.get('uid')
    row_dict = models.Order.objects.filter(id=uid).values('title', 'price', 'status').first()
    if not row_dict:
        return JsonResponse({'status': False, 'error': '抱歉！数据不存在'})

    result = {
        'status': True,
        'data': row_dict
    }
    return JsonResponse(result)


@csrf_exempt
def order_edit(request):

    """编辑订单"""

    uid = request.GET.get('uid')
    row_object = models.Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({'status': False, 'tips': '抱歉！数据不存在'})

    form = OrderModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'error': form.errors})










