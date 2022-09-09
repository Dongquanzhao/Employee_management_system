from django.shortcuts import render, HttpResponse, redirect
from django import forms

from io import BytesIO

from RedemptionII.utils.bootstrap import BootstrapForm
from RedemptionII.utils.Encrypt import md5
from RedemptionII import models
from RedemptionII.utils.code import check_code


class LoginForm(BootstrapForm):
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput,
        required=True   # 表示必填
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(render_value=True),
        required=True
    )
    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput,
        required=True  # 表示必填
    )

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)


def login(request):

    """登录"""

    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(data=request.POST)
    if form.is_valid():

        # 验证码校验
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code', "")
        if code.upper() != user_input_code.upper():
            form.add_error('code', "验证码错误！")
            return render(request, 'login.html', {'form': form})

        # 去数据库校验用户名和密码是否正确，获取用户对象：None
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:

            # 主动显示错误
            form.add_error('password', '用户名或密码错误')
            return render(request, 'login.html', {'form': form})

        # 用户名和密码正确
        # 网站生成随机字符串：写到用户浏览器的cookie中；再写入到session中
        request.session['info'] = {'id': admin_object.id, 'name': admin_object.username}

        # 设置7天免登录
        request.session.set_expiry(60 * 60 * 24 * 7)
        return redirect('/admin/list/')
    return render(request, 'login.html', {'form': form})


def logout(request):

    """注销"""

    request.session.clear()

    return redirect('/login/')


def image_code(request):

    """生成图片验证码"""

    # 调用 pillow 函数，生成图片
    img, code_string = check_code()

    # 写入到自己的 session 中，以便后续获取验证码再进行校验
    request.session['image_code'] = code_string

    # 给 Session 设置60秒超时
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())






















