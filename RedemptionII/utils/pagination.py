"""
自定义分类组件
(若以后想使用这个分页组件，需要做以下几件事)

在视图函数中：

def pretty_list(request):

    # 1.根据自己的情况去筛选自己的数据
    queryset = models.PrettyNum.objects.all()

    # 2.实例化分页对象
    page_object = Pagination(request, queryset)

    context = {
         'search_data': search_data,
         'queryset': page_object.page_queryset,  # 分完页的数据
         'page_string': page_object.html(),         # 生成的页码
    }

    return render(request, 'pretty_list.html', context)

在 HTML 页面中：

    {% for obj in queryset %}
        {{obj.xxx}}
    {% endfor %}


    <ul class="pagination">
        {{ page_string }}
     </ul>

"""

from django.utils.safestring import mark_safe


class Pagination(object):

    def __init__(self, request, queryset, page_size=10, page_param="page", plus=5):

        """
        :param request: 请求的对象
        :param queryset: 符合条件的数据(根据这个数据进行分页处理)
        :param page_size: 每页显示多少条数据
        :param page_param: 在 URL 中传送的获取分页的参数，例如： /pretty/list/?page=2
        :param plus: 显示当前页的前几页或后几页(根据页码)
        """

        # 解决搜索的时候分页按钮显示不对的 bug
        import copy
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict
        self.page_param = page_param
        # query_dict.setlist('page', [21])
        # print(query_dict.urlencode())

        page = request.GET.get(page_param, '1')
        if page.isdecimal():
            page = int(page)
        else:
            page = 1

        self.page = page
        self.page_size = page_size

        self.start = (page - 1) * page_size
        self.end = page * page_size

        self.page_queryset = queryset[self.start:self.end]

        # 获取数据总条数
        total_count = queryset.count()

        # 获取总页码
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count
        self.plus = plus

    def html(self):

        # 通过计算，显示当前页的前5页和后5页
        if self.total_page_count <= 2 * self.plus + 1:

            # 数据库数据较少
            start_page = 1
            end_page = self.total_page_count
        else:

            # 数据库数据较多

            # 当前页 <5时(小极值)
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus
            else:

                # 当前页 >5
                # 当前页 +5 > 总页面
                if (self.page + self.plus) > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        # 页码按钮
        page_str_list = []
        self.query_dict.setlist(self.page_param, [1])

        # 跳到首页
        page_str_list.append('<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))

        # 获取上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        else:

            # 第一页的上一页固定为1
            self.query_dict.setlist(self.page_param, [1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)

        # for i in range(1, total_page_count + 1):
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = ' <li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = ' <li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)

        # 获取下一页
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])

            prev = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        else:

            # 最后一页的固定值为总页数
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            prev = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)

        # 跳到尾页
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        page_str_list.append('<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))

        """
        <li><a href="?page=1">1</a></li>
        <li><a href="?page=2">2</a></li>
        <li><a href="?page=3">3</a></li>
        <li><a href="?page=4">4</a></li>
        <li><a href="?page=5">5</a></li>
        """

        search_string = """
            <li>
                <form style="float: left; margin-left: -1px" method="get">
                    <input name="page"
                           style="position: relative;float: left;display: inline-block; width: 80px;border-radius: 0;"
                           type="text" class="form-control" placeholder="页码">
                    <button style="border-radius: 0" class="btn btn-default" type="submit">跳转</button>
                </form>
            </li>
            """

        page_str_list.append(search_string)
        page_string = mark_safe("".join(page_str_list))
        return page_string