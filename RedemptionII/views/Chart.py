from django.shortcuts import render
from django.http import JsonResponse


def chart_list(request):
    """数据统计页面"""

    return render(request, 'chart_list.html')


def chart_bar(request):
    """构造柱状图数据"""

    legend = ['亚瑟摩根', '约翰马斯顿']
    series_list = [
        {
            "name": '亚瑟摩根',
            'type': 'bar',
            "data": [5, 20, 36, 10, 10, 20]
        },
        {
            "name": '约翰马斯顿',
            'type': 'bar',
            'data': [5, 20, 36, 10, 10, 20]
        },
    ]
    x_axis = ['1月', '2月', '3月', '4月', '5月', '6月', '7月']

    result = {
        'status': True,
        'data': {
            'legend': legend,
            'series_list': series_list,
            'x_axis': x_axis,
        }
    }

    return JsonResponse(result)


def chart_pie(request):
    """构造饼状图"""

    db_data_list = [
        {'value': 1048, 'name': 'IT部'},
        {'value': 735, 'name': '策划部'},
        {'value': 580, 'name': '销售部'},
    ]
    result = {
        'status': True,
        'data': db_data_list,
    }

    return JsonResponse(result)


def chart_line(request):
    """构造饼状图数据"""

    legend = ['梵蒂冈', '索马里']
    series_list = [
        {
            "name": '梵蒂冈',
            'type': 'line',
            'stack': 'Total',
            "data": [5, 20, 36, 10, 10, 20]
        },
        {
            "name": '索马里',
            'type': 'line',
            'stack': 'Total',
            'data': [5, 20, 36, 10, 10, 20]
        },
    ]
    x_axis = ['1月', '2月', '3月', '4月', '5月', '6月', '7月']

    result = {
        'status': True,
        'data': {
            'legend': legend,
            'series_list': series_list,
            'x_axis': x_axis,
        }
    }

    return JsonResponse(result)


def hightcharts(request):
    """hightcharts示例"""

    return render(request, 'hightcharts.html')
