# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

from config import fields


class SchoolFellow(models.Model):
    name = models.CharField(max_length=30, null=False, verbose_name=fields[0])
    sex = models.CharField(max_length=1, null=False, verbose_name=fields[1])
    tell = models.CharField(max_length=11, null=True, verbose_name=fields[2])
    fixed_tell = models.CharField(max_length=12, null=True, verbose_name=fields[3])
    email = models.EmailField(null=False, verbose_name=fields[4])
    department = models.CharField(max_length=100, null=False, verbose_name=fields[5])
    school_class = models.CharField(max_length=30, blank=True, null=True, verbose_name=fields[6])
    education = models.CharField(max_length=50, null=False, verbose_name=fields[7])
    year_system = models.CharField(max_length=30, blank=True, null=True, verbose_name=fields[8])
    year_enroll = models.IntegerField(null=False, verbose_name=fields[9])
    year_graduate = models.IntegerField(null=False, verbose_name=fields[10])
    teacher = models.CharField(max_length=40, blank=True, null=True, verbose_name=fields[11])
    mentor = models.CharField(max_length=40, blank=True, null=True, verbose_name=fields[12])
    current_work_unit = models.CharField(max_length=100, null=False, verbose_name=fields[13])
    address_work_unit = models.CharField(max_length=200, blank=True, null=True, verbose_name=fields[14])
    industry_category = models.CharField(max_length=20, blank=True, null=True, verbose_name=fields[15])
    unit_property = models.CharField(max_length=30, blank=True, null=True, verbose_name=fields[16])
    current_job_title = models.CharField(max_length=100, blank=True, null=True, verbose_name=fields[17])
    honour = models.TextField(blank=True, verbose_name=fields[18], default="无")
    remark = models.TextField(blank=True, verbose_name=fields[19], default="无")
    last_submit = models.DateTimeField(blank=True, verbose_name="上一次修改时间", auto_now=True)
    last_changed_fields = models.TextField(verbose_name="修改项", blank=True)

    class Meta:
        verbose_name = "校友"
        verbose_name_plural = "校友们"

    def __str__(self):
        return self.name


class Account(AbstractUser):
    information = models.ForeignKey(blank=True, verbose_name="所关联的详细个人信息", to=SchoolFellow, on_delete=models.CASCADE,
                                    null=True,
                                    )

    def __str__(self):
        return self.username
