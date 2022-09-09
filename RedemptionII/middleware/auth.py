from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class AuthMiddleWare(MiddlewareMixin):

    def process_request(self, request):

        # 排除那些不需要登陆就能访问的页面
        # request.path_info 能够获取当前用户请求的 URL
        if request.path_info in ['/login/', '/image/code/']:
            return

        # 读取当前访问用户的 session 信息，若能读到则继续向后走
        info_dict = request.session.get('info')
        if info_dict:
            return

        # 没有登录过,返回登陆界面
        return redirect('/login/')

