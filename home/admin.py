# Register your models here.
from datetime import date

from django.contrib import admin

from config import fields
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
    list_display = ['name', 'sex', 'tell', 'fixed_tell', 'email', 'department', 'school_class', 'education',
                    'year_system', 'year_enroll', 'year_graduate', 'teacher', 'mentor', 'current_work_unit',
                    'address_work_unit', 'industry_category', 'unit_property', 'current_job_title', 'honour', 'remark']
    list_filter = ['sex', 'department', 'education', 'year_system', 'year_enroll', 'year_graduate', 'industry_category',
                   'unit_property', ]
    search_fields = list_display


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['username', '所关联的详细个人信息']

    def 所关联的详细个人信息(self, obj):
        if obj.is_staff:
            return "超级用户没有关联的详细个人信息"
        else:
            return obj.information

    list_display_links = ['username', '所关联的详细个人信息']


admin.site.site_header = "校友信息填报系统__后台管理"
admin.site.site_url = None
