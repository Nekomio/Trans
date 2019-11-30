# Register your models here.
from datetime import date

from django.contrib import admin

from config import FIELDS
from home.models import SchoolFellow


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
    list_filter = [filterByGraduate, ] + FIELDS
    search_fields = FIELDS
    fields = list_display

    def view_on_site(self, obj=None):
        return 'back/logout'


admin.site.site_header = "校友信息填报系统__后台管理"
