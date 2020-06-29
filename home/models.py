# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

from config import fields


class SchoolFellow(models.Model):
    i = 0
    name = models.CharField(max_length=30, null=False, verbose_name=fields[i + 0])
    sex_id = models.CharField(max_length=1, null=False, verbose_name=fields[i + 1])
    tell = models.CharField(blank=True, max_length=12, null=True, verbose_name=fields[i + 2])
    i = 0
    email = models.EmailField(null=False, verbose_name=fields[i + 3])
    
    # department = models.CharField(max_length=100, null=False, verbose_name=fields[i + 4])
    # school_class = models.CharField(max_length=30, blank=True, null=True, verbose_name=fields[i + 5])
    # education = models.CharField(max_length=50, null=False, verbose_name=fields[i + 6])
    # year_system = models.CharField(max_length=30, blank=True, null=True, verbose_name=fields[i + 7])
    # year_enroll = models.IntegerField(null=False, verbose_name=fields[i + 8])
    # year_graduate = models.IntegerField(null=False, verbose_name=fields[i + 9])
    # teacher = models.CharField(max_length=40, blank=True, null=True, verbose_name=fields[i + 10])
    # mentor = models.CharField(max_length=40, blank=True, null=True, verbose_name=fields[i + 11])

    department1 = models.CharField(max_length=100, null=False, verbose_name=fields[i + 4])
    school_class1 = models.CharField(max_length=30, blank=True, null=True, verbose_name=fields[i + 5])
    education1 = models.CharField(max_length=50, null=False, verbose_name=fields[i + 6])
    year_system1 = models.CharField(max_length=30, blank=True, null=True, verbose_name=fields[i + 7])
    year_enroll1 = models.IntegerField(null=False, verbose_name=fields[i + 8])
    year_graduate1 = models.IntegerField(null=False, verbose_name=fields[i + 9])
    teacher1 = models.CharField(max_length=40, blank=True, null=True, verbose_name=fields[i + 10])
    mentor1 = models.CharField(max_length=40, blank=True, null=True, verbose_name=fields[i + 11])

    department2 = models.CharField(max_length=100, null=False, verbose_name=fields[i + 12])
    school_class2 = models.CharField(max_length=30, blank=True, null=True, verbose_name=fields[i + 13])
    education2 = models.CharField(max_length=50, null=False, verbose_name=fields[i + 14])
    year_system2 = models.CharField(max_length=30, blank=True, null=True, verbose_name=fields[i + 15])
    year_enroll2 = models.IntegerField(null=False, verbose_name=fields[i + 16])
    year_graduate2 = models.IntegerField(null=False, verbose_name=fields[i + 17])
    teacher2 = models.CharField(max_length=40, blank=True, null=True, verbose_name=fields[i + 18])
    mentor2 = models.CharField(max_length=40, blank=True, null=True, verbose_name=fields[i + 19])

    department3 = models.CharField(max_length=100, null=False, verbose_name=fields[i + 20])
    school_class3 = models.CharField(max_length=30, blank=True, null=True, verbose_name=fields[i + 21])
    education3 = models.CharField(max_length=50, null=False, verbose_name=fields[i + 22])
    year_system3 = models.CharField(max_length=30, blank=True, null=True, verbose_name=fields[i + 23])
    year_enroll3 = models.IntegerField(null=False, verbose_name=fields[i + 24])
    year_graduate3 = models.IntegerField(null=False, verbose_name=fields[i + 25])
    teacher3 = models.CharField(max_length=40, blank=True, null=True, verbose_name=fields[i + 26])
    mentor3 = models.CharField(max_length=40, blank=True, null=True, verbose_name=fields[i + 27])
    current_work_unit = models.CharField(max_length=100, null=False, verbose_name=fields[i + 12])
    address_work_unit = models.CharField(max_length=200, blank=True, null=True, verbose_name=fields[i + 13])
    industry_category = models.CharField(max_length=20, blank=True, null=True, verbose_name=fields[i + 14])
    unit_property = models.CharField(max_length=30, blank=True, null=True, verbose_name=fields[i + 15])
    current_job_title = models.CharField(max_length=100, blank=True, null=True, verbose_name=fields[i + 16])
    honour = models.TextField(blank=True, verbose_name=fields[i + 17], default="无")
    remark = models.TextField(blank=True, verbose_name=fields[i + 18], default="无")
    
    current_work_unit = models.CharField(max_length=100, null=False, verbose_name=fields[i + 28])
    address_work_unit = models.CharField(max_length=200, blank=True, null=True, verbose_name=fields[i + 29])
    industry_category = models.CharField(max_length=20, blank=True, null=True, verbose_name=fields[i + 30])
    unit_property = models.CharField(max_length=30, blank=True, null=True, verbose_name=fields[i + 31])
    current_job_title = models.CharField(max_length=100, blank=True, null=True, verbose_name=fields[i + 32])
    honour = models.TextField(blank=True, verbose_name=fields[i + 33], default="无")
    remark = models.TextField(blank=True, verbose_name=fields[i + 34], default="无")
    last_submit = models.DateTimeField(blank=True, verbose_name="上一次修改时间")
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
