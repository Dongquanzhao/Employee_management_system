from RedemptionII import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django import forms
from RedemptionII.utils.bootstrap import BootstrapModelForm


class UserModelForm(BootstrapModelForm):
    name = forms.CharField(
        min_length=3,
        label='用户名',
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'age', 'account', 'create_time', 'gender', 'depart']

        # # 加样式的旧方法
        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'form-control'}),
        #     'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        #     'age': forms.TextInput(attrs={'class': 'form-control'}),
        # }


class PrettyModelForm(BootstrapModelForm):

    # # 验证：方式1(基于正则表达式)
    # mobile = forms.CharField(
    #     label='手机号',
    #     validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')],
    # )

    class Meta:
        model = models.PrettyNum

        # # 选出所有字段
        # fields = "__all__"

        # 选出想要的字段
        fields = ["mobile", 'price', 'level', 'status']

        # # 选出除特定字段以外的所有字段
        # exclude = ['level']

    # 验证：方式2(基于钩子方法)
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']

        # 验证手机号是否存在
        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError('手机号已经存在')

        if len(txt_mobile) != 11:

            # 验证不通过
            raise ValidationError("格式错误！！！")

        # 验证通过，返回用户输入的值
        return txt_mobile


class PrettyEditModelForm(BootstrapModelForm):

    # # 让手机号变成不可编辑状态
    # mobile = forms.CharField(disabled=True, label='手机号')

    # 验证：方式1(基于正则表达式)
    mobile = forms.CharField(
        label='手机号',
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')],
    )

    class Meta:
        model = models.PrettyNum

        # # 选出所有字段
        # fields = "__all__"

        # 选出想要的字段
        fields = ['mobile', 'price', 'level', 'status']

        # # 选出除特定字段以外的所有字段
        # exclude = ['level']

    # 验证：方式2(基于钩子方法)
    def clean_mobile(self):

        # # 表示当前编辑的那一行的 ID
        # print(self.instance.pk)

        txt_mobile = self.cleaned_data['mobile']

        # 验证手机号是否存在(排除自身)
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError('手机号已经存在')

        # if len(txt_mobile) != 11:
        #
        #     # 验证不通过
        #     raise ValidationError("格式错误！！！")

        # 验证通过，用户输入的值返回
        return txt_mobile