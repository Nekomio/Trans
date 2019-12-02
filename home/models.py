# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class SchoolFellow(models.Model):
    name = models.CharField(max_length=30, null=False)
    sex = models.CharField(max_length=1, null=False)
    tell = models.CharField(max_length=11, null=True)
    fixed_tell = models.CharField(max_length=12, null=True)
    email = models.EmailField(null=False)
    department = models.CharField(max_length=100, null=False)
    school_class = models.CharField(max_length=30, null=True)
    education = models.CharField(max_length=50, null=False)
    year_system = models.IntegerField(null=True)
    year_enroll = models.DateField(null=False)
    year_graduate = models.DateField(null=False)
    teacher = models.CharField(max_length=40, null=True)
    mentor = models.CharField(max_length=40, null=True)
    current_work_unit = models.CharField(max_length=100, null=False)
    address_work_unit = models.CharField(max_length=200, null=True)
    industry_category = models.CharField(max_length=20, null=True)
    unit_property = models.CharField(max_length=30, null=True)
    current_job_title = models.CharField(max_length=100, null=True)
    honour = models.TextField(null=True)
    remark = models.TextField(null=True)

    class Meta:
        verbose_name = "校友"
        verbose_name_plural = "校友们"

    def __str__(self):
        return self.name


class Account(AbstractUser):
    information = models.ForeignKey(to=SchoolFellow, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return self.username
