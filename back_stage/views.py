import csv
from datetime import datetime
from io import BytesIO

from django.http import HttpResponse
from xlwt import Workbook, XFStyle

# Create your views here.
from config import FIELDS
from home.models import SchoolFellow


def login(request):
    return HttpResponse("this is back_stage login.")


def get_excel(request):
    fellows = SchoolFellow.objects.order_by('姓名')
    print(fellows[0].姓名)
    ws = Workbook(encoding="utf-8")
    w = ws.add_sheet(u"校友信息导出表")
    for i in FIELDS:
        w.write(0, FIELDS.index(i), i)
    for i in range(len(fellows)):
        w.write(i + 1, 0, fellows[i].姓名)
        w.write(i + 1, 1, fellows[i].性别)
        w.write(i + 1, 2, fellows[i].联系方式)
        w.write(i + 1, 3, fellows[i].电子邮箱)
        w.write(i + 1, 4, fellows[i].院系)
        w.write(i + 1, 5, fellows[i].班级)
        w.write(i + 1, 6, fellows[i].学历)
        w.write(i + 1, 7, fellows[i].学制)
        x = datetime.strftime(fellows[i].入学年份, '%Y-%m-%d')
        print(x)
        w.write(i + 1, 8, x)
        print(type(fellows[i].入学年份))
        dateFormat = XFStyle()
        dateFormat.num_format_str = 'yyyy/mm/dd'
        w.write(i + 1, 9, fellows[i].毕业年份, dateFormat)
        w.write(i + 1, 10, fellows[i].辅导员老师或印象最深刻的任课老师)
        w.write(i + 1, 11, fellows[i].现工作单位)
        w.write(i + 1, 12, fellows[i].工作单位地址)
        w.write(i + 1, 13, fellows[i].行业类别)
        w.write(i + 1, 14, fellows[i].单位性质)
        w.write(i + 1, 15, fellows[i].现职务职称)
        w.write(i + 1, 16, fellows[i].所获荣誉)
        w.write(i + 1, 17, fellows[i].备注)
    sio = BytesIO()
    ws.save(sio)
    sio.seek(0)
    res = HttpResponse(sio.getvalue(), content_type="application/vnd.ms-excel")
    sio.close()
    res['Content-Disposition'] = 'attachment;filename = school_fellow_information_export_table.xls'
    return res


def logout(request):
    return HttpResponse("this is back_stage.logout")


def home(request):
    response = HttpResponse(content_type='text/csv')
    # response['mimetype'] = 'text/csv'
    response['Content-Disposition'] = 'attachment;filename = school_fellow_information_export_table.csv'

    writer = csv.writer(response)
    writer.writerow(['姓名', '性别'])
    print(response['Content-Disposition'])
    return response
