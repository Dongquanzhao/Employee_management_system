from django.shortcuts import render, redirect
from RedemptionII import  models
from RedemptionII.utils.pagination import Pagination
from RedemptionII.utils.form import UserModelForm, PrettyModelForm, PrettyEditModelForm

# Create your views here.


def pretty_list(request):

    """靓号列表"""

    # # 一口气创建多个靓号
    # for i in range(300):
    #     models.PrettyNum.objects.create(mobile='13100572930', price=9999, level=4, status=1)


    # # 按条件搜索某个靓号: 方式1
    # queryset1 = models.PrettyNum.objects.filter(mobile='19178521061', id=2)
    # print(queryset1)
    #
    # # 按条件搜索某个靓号：方式2
    # # 传入空字典相当于获取所有
    # data_dict = {'mobile': '19178521062', 'id': 3}
    # queryset2 = models.PrettyNum.objects.filter(**data_dict)
    # print(queryset2)

    # # 在 url 上搜索手机号
    data_dict = {}
    search_data = request.GET.get('q')
    if search_data:
        data_dict['mobile__contains'] = search_data
    # res = models.PrettyNum.objects.filter(**data_dict)
    # print(res)



    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")
    page_object = Pagination(request, queryset)
    context = {
         'search_data': search_data,
         'queryset': page_object.page_queryset,  # 分完页的数据
         'page_string': page_object.html(),         # 生成的页码
    }

    # select * from 表 order by level desc;

    # # 在 url 上跳转到特定页
    # page = int(request.GET.get('page', 1))
    #
    # # 每页显示10条数据
    # page_size = 10
    # start = (page - 1) * page_size
    # end = page * page_size


    # # 通过计算，显示当前页的前5页和后5页
    # plus = 5
    # if total_page_count <=2 * plus + 1:
    #
    #     # 数据库数据较少
    #     start_page = 1
    #     end_page = total_page_count + 1
    # else:
    #
    #     # 数据库数据较多
    #
    #     # 当前页 <5时(小极值)
    #     if page <= plus:
    #         start_page = 1
    #         end_page = 2 * plus
    #     else:
    #
    #         # 当前页 >5
    #         # 当前页 +5 > 总页面
    #         if(page + plus) > total_page_count:
    #             start_page = total_page_count - 2 * plus
    #             end_page = total_page_count
    #         else:
    #             start_page = page - plus
    #             end_page = page + plus
    #
    # # 页码按钮
    # page_str_list = []
    #
    # # 跳到首页
    # page_str_list.append('<li><a href="?page={}">首页</a></li>'.format(1))
    #
    # # 获取上一页
    # if page > 1:
    #     prev = '<li><a href="?page={}">上一页</a></li>'.format(page - 1)
    # else:
    #
    #     # 第一页的上一页固定为1
    #     prev = '<li><a href="?page={}">上一页</a></li>'.format(1)
    # page_str_list.append(prev)
    #
    #
    # # for i in range(1, total_page_count + 1):
    # for i in range(start_page, end_page + 1):
    #     if i == page:
    #         ele = ' <li class="active"><a href="?page={}">{}</a></li>'.format(i, i)
    #     else:
    #         ele = ' <li><a href="?page={}">{}</a></li>'.format(i, i)
    #     page_str_list.append(ele)
    #
    # # 获取下一页
    # if page < total_page_count:
    #     prev = '<li><a href="?page={}">下一页</a></li>'.format(page + 1)
    # else:
    #
    #     # 最后一页的固定值为总页数
    #     prev = '<li><a href="?page={}">下一页</a></li>'.format(total_page_count)
    # page_str_list.append(prev)
    #
    # # 跳到尾页
    # page_str_list.append('<li><a href="?page={}">尾页</a></li>'.format(total_page_count))
    #
    # """
    # <li><a href="?page=1">1</a></li>
    # <li><a href="?page=2">2</a></li>
    # <li><a href="?page=3">3</a></li>
    # <li><a href="?page=4">4</a></li>
    # <li><a href="?page=5">5</a></li>
    # """
    #
    # search_string = """
    # <li>
    #     <form style="float: left; margin-left: -1px" method="get">
    #         <input name="page"
    #                style="position: relative;float: left;display: inline-block; width: 80px;border-radius: 0;"
    #                type="text" class="form-control" placeholder="页码">
    #         <button style="border-radius: 0" class="btn btn-default" type="submit">跳转</button>
    #     </form>
    # </li>
    # """
    #
    # page_str_list.append(search_string)
    # page_string = mark_safe("".join(page_str_list))

    return render(request, 'pretty_list.html', context)


def pretty_add(request):

    """添加靓号"""
    if request.method == 'GET':
        form = PrettyModelForm()
        return render(request, 'pretty_add.html', {'form': form})
    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request, 'pretty_add.html', {'form': form})


def pretty_edit(request, nid):

    """编辑靓号"""

    row_object = models.PrettyNum.objects.filter(id=nid).first()

    if request.method == 'GET':
        form = PrettyEditModelForm(instance=row_object)
        return render(request, 'pretty_edit.html', {"form": form})

    form = PrettyEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')

    return render(request, 'pretty_edit.html', {'form': form})


def pretty_delete(request, nid):

    """删除靓号"""

    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/pretty/list/')

