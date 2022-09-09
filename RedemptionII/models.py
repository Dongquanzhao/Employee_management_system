from django.db import models

# Create your models here.


class Admin(models.Model):

    """管理员"""
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)

    def __str__(self):
        return self.username


class Department(models.Model):

    """部门表"""
    title = models.CharField(verbose_name='标题', max_length=32)

    # 输出对象名称
    def __str__(self):
        return self.title


class UserInfo(models.Model):

    """员工表"""
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    # create_time = models.DateTimeField(verbose_name="入职时间")
    create_time = models.DateField(verbose_name="入职时间")

    # 无约束地设置 ID
    #

    # 有约束地设置ID
    # to 表示与哪张表关联
    # to_field 与表中的哪一列关联

    # 虽然写的是 depart ，但 django 会自动生成数据列 depart_id
    # depart = models.ForeignKey(to="Department", to_field="id")

    # 当部门被删除
    # ## 解决方案1：级联删除
    # depart = models.ForeignKey(to="Department", to_field="id", on_delete=models.CASCADE)
    # ##解决方案2： 直接置空
    depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", null=True, on_delete=models.SET_NULL)

    # 可在 django 中做约束
    gender_choices = (
        (1, '男'),
        (2, '女'),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)


class PrettyNum(models.Model):

    """靓号表"""

    mobile = models.CharField(verbose_name="手机号", max_length=11)

    # 想要允许为空，要在参数中加上 null=True, blank=True
    price = models.IntegerField(verbose_name="价格", default=0)

    # 靓号级别
    level_choices = (
        (1, "1级"),
        (2, "2级"),
        (3, "3级"),
        (4, "4级"),
    )

    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)

    # 靓号现在的状态
    status_choices = (
        (1, "已占用"),
        (2, "未使用"),
    )

    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=2)


class Task(models.Model):

    """任务列表"""

    level_choices = (
        (1, '紧急'),
        (2, '重要'),
        (3, '一般'),
    )
    level = models.SmallIntegerField(verbose_name='级别', choices=level_choices, default=3)
    title = models.CharField(verbose_name='标题', max_length=64)
    detail = models.TextField(verbose_name='任务详情')

    # 会生成 user_id 这一列
    user = models.ForeignKey(verbose_name='任务负责人', to='Admin', on_delete=models.CASCADE)


class Order(models.Model):

    """订单"""

    oid = models.CharField(verbose_name='订单号', max_length=64)
    title = models.CharField(verbose_name='名单', max_length=32)
    price = models.IntegerField(verbose_name='价格')

    status_choices = (
        (1, '待支付'),
        (2, '已支付'),
    )
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choices, default=1)

    # 会生成 admin_id
    admin = models.ForeignKey(verbose_name='管理员', to='Admin', on_delete=models.CASCADE)


class BestEmployee(models.Model):
    """最佳员工"""

    name = models.CharField(verbose_name='姓名', max_length=32)
    age = models.IntegerField(verbose_name='年龄')
    img = models.CharField(verbose_name='头像', max_length=128)


class BestTeam(models.Model):
    """最佳员工"""

    name = models.CharField(verbose_name='团队名', max_length=32)
    count = models.IntegerField(verbose_name='成员数量')

    # 本质上数据库也是 CharField
    img = models.FileField(verbose_name='LOGO', max_length=128, upload_to='team/')

















