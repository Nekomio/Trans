# Register your models here.
from datetime import date

from django.contrib import admin

from config import FIELDS
from home.models import SchoolFellow, Account


class filterByGraduate(admin.SimpleListFilter):
    title = ('毕业年份')
    parameter_name = '毕业年份'

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request)
        lst = []
        if qs.filter(毕业年份__gte=date(2019, 1, 1), 毕业年份__lte=date(2019, 12, 31)):
            lst += [('this year', ('今年毕业的所有人'))]
        if qs.filter(毕业年份__gte=date(2018, 1, 1), 毕业年份__lte=date(2018, 12, 31)):
            lst += [('last year', ('去年毕业的所有人'))]
        return lst

    def queryset(self, request, queryset):
        if self.value() == 'this year':
            return queryset.filter(毕业年份__gte=date(2019, 1, 1), 毕业年份__lte=date(2019, 12, 31))
        if self.value() == 'last year':
            return queryset.filter(毕业年份__gte=date(2018, 1, 1), 毕业年份__lte=date(2018, 12, 31))


@admin.register(SchoolFellow)
class SchoolFellowAdmin(admin.ModelAdmin):
    list_display = FIELDS

    def 姓名(self, obj):
        return obj.name

    def 性别(self, obj):
        return obj.sex

    def 移动电话(self, obj):
        return obj.tell

    def 固定电话(self, obj):
        return obj.fixed_tell

    def 电子邮箱(self, obj):
        return obj.email

    # def
    # list_display = FIELDS
    # list_filter = [filterByGraduate, ] + FIELDS
    # search_fields = FIELDS
    # fields = list_display


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['username', '关联的详细个人信息', '性别']

    def 性别(self, obj):
        if obj.information:
            return obj.information.性别
        else:
            return "超级用户没有性别之分"

    def 关联的详细个人信息(self, obj):
        if obj.information:
            return obj.information.姓名
        else:
            return "超级用户没有详细信息"


admin.site.site_header = "校友信息填报系统__后台管理"
admin.site.site_url = None
