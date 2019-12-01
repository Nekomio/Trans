# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


# name = models.CharField(name="姓名", max_length=30, null=False)
# sex = models.BooleanField(name="性别", null=False)
# tell = models.CharField(name="联系方式", max_length=11, null=False)
# email = models.EmailField(name="电子邮箱", null=False)
# department = models.CharField(name="院系", max_length=100, null=False)
# school_class = models.CharField(name="班级", max_length=30, null=True)
# education = models.CharField(name="学历", max_length=50, null=False, default="本科学生")
# year = models.IntegerField(name="学制", null=True)
# start = models.DateField(name="入学年份", null=False)
# graduate = models.DateField(name="毕业年份", null=False)
# teacher = models.CharField(name="辅导员老师或印象最深刻的任课老师", max_length=40, null=True)
# work_place = models.CharField(name="现工作单位", max_length=100, null=False)
# address = models.CharField(name="工作单位地址", max_length=200, null=True)
# category = models.CharField(name="行业类别", max_length=20, null=True)
# work_property = models.CharField(name="单位性质", max_length=30, null=True)
# title = models.CharField(name="现职务职称", max_length=100, null=True)
# honour = models.TextField(name="所获荣誉", null=True)
# comments = models.TextField(name="备注", null=True)


class SchoolFellow(models.Model):
    name = models.CharField(name="姓名", max_length=30, null=False)
    sex = models.CharField(name="性别", max_length=1, null=False, default="男")
    tell = models.CharField(name="联系方式", max_length=11, null=False)
    email = models.EmailField(name="电子邮箱", null=False)
    department = models.CharField(name="院系", max_length=100, null=False)
    school_class = models.CharField(name="班级", max_length=30, null=True)
    education = models.CharField(name="学历", max_length=50, null=False, default="本科学生")
    year = models.IntegerField(name="学制", null=True)
    start = models.DateField(name="入学年份", null=False)
    graduate = models.DateField(name="毕业年份", null=False)
    teacher = models.CharField(name="辅导员老师或印象最深刻的任课老师", max_length=40, null=True)
    work_place = models.CharField(name="现工作单位", max_length=100, null=False)
    address = models.CharField(name="工作单位地址", max_length=200, null=True)
    category = models.CharField(name="行业类别", max_length=20, null=True)
    work_property = models.CharField(name="单位性质", max_length=30, null=True)
    title = models.CharField(name="现职务职称", max_length=100, null=True)
    honour = models.TextField(name="所获荣誉", null=True)
    comments = models.TextField(name="备注", null=True)

    class Meta:
        verbose_name = "校友"
        verbose_name_plural = "校友们"

    def __str__(self):
        return self.姓名


class Account(AbstractUser):
    information = models.ForeignKey(to=SchoolFellow, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return self.username
