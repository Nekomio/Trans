import os
from datetime import datetime
from io import BytesIO

from django.contrib import auth
from django.contrib.auth.decorators import login_required, permission_required
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from xlwt import Workbook, XFStyle

from AIR_System.settings import STATIC_ROOT
from config import fields
from home.models import Account, SchoolFellow
from utils.ChekCode import CheckCode

Obj_code = CheckCode()


def register(request):
    resp = {'error_msg': "", 'passcode_src': "", 'name': "", 'password': ""}
    session_key = str(hash(request.META['REMOTE_ADDR']))
    src = "%s.png" % session_key
    resp['passcode_src'] = src
    path = os.path.join(STATIC_ROOT, src)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        passcode = request.POST['passcode']
        print(username, password)

        if request.session[session_key] != passcode:
            resp['error_msg'] = "验证码不匹配"
        else:
            if username and password:
                if Account.objects.filter(username=username):
                    resp['error_msg'] = "用户已存在"
                else:
                    user = Account.objects.create_user(username=username, password=password)
                    user.save()
                    # 添加一些权限

                    #
                    resp['error_msg'] = "注册成功"
                    auth.login(request, user)
                    return redirect(to="user.information")
            else:
                resp['error_msg'] = '用户名或密码不能为空，请正确输入'
        resp['name'] = username
        resp['password'] = password
        passcode = Obj_code.gene_code(path)
        print(session_key, passcode)
        request.session[session_key] = passcode
        return render(request, 'register.html', resp)

    if request.method == "GET":
        passcode = Obj_code.gene_code(path)
        print(session_key, passcode)
        request.session[session_key] = passcode
        return render(request, 'register.html', resp)


def login(request):
    resp = {'error_msg': "", 'passcode_src': "", 'name': "", 'password': ""}
    session_key = str(hash(request.META['REMOTE_ADDR']))
    src = "%s.png" % session_key
    resp['passcode_src'] = src
    path = os.path.join(STATIC_ROOT, src)
    if request.method == "POST":
        print("has printed：post:", request.POST)
        username = request.POST['username']
        password = request.POST['password']
        passcode = request.POST['passcode']
        if request.session[session_key] != passcode:
            resp['error_msg'] = "验证码不匹配"
        else:
            print(username, password)
            if Account.objects.filter(username=username):
                account = auth.authenticate(username=username, password=password)
                print("authenticated:", account)
                if account:
                    if account.is_active:
                        auth.login(request, account)
                        return redirect(to="user.information")
                    else:
                        resp['error_msg'] = "the account is not active."
                else:
                    resp['error_msg'] = "密码错误"
            else:
                resp['error_msg'] = "用户不存在"
        passcode = Obj_code.gene_code(path)
        print(session_key, passcode)
        request.session[session_key] = passcode
        resp['name'] = username
        resp['password'] = password
        return render(request, 'login.html', resp)
        # users = Account.objects.get_by_natural_key(username=username)
        # user = auth.authenticate(request,username=username,password=password)
        # print(user)
        # print(users)
    if request.method == "GET":
        # print("has printed GET:", request.GET)
        passcode = Obj_code.gene_code(path)
        print(session_key, passcode)
        request.session[session_key] = passcode
        return render(request, "login.html", resp)


@login_required(login_url='user.login')
def logout(request):
    auth.logout(request)
    return redirect(to="user.logout")


@login_required(login_url='user.login')
def information_filling(request):
    information = request.user.information
    print("user:", request.user)
    print(information)
    if request.method == "POST":
        print(request.POST)
        dic = request.POST
        if not information:
            information = SchoolFellow()
        switch = {
            '1': "男",
            "2": "女",
        }
        switch1 = {
            "1": "本科生",
            "2": "硕士研究生",
            "3": "博士生",
        }
        switch2 = {
            "1": "机关",
            "2": "事业单位",
            "3": "企业",
            "4": "其他",
        }
        information.name = dic['name']
        information.tell = dic['tell']
        information.sex = switch[dic['sex']]
        information.email = dic['email']
        information.department = dic['department']
        information.school_class = dic['class']
        information.education = switch1[dic['education']]
        information.year_system = dic['year']
        information.year_enroll = datetime.strptime(dic['start'], "%Y-%m-%d")
        information.year_graduate = datetime.strptime(dic['graduate'], "%Y-%m-%d")
        try:
            information.teacher = dic['teacher']
        except:
            information.mentor = dic['mentor']
        information.current_work_unit = dic['workplace']
        information.address_work_unit = dic['address']
        information.industry_category = switch2[dic['category']]
        information.unit_property = dic['property']
        information.current_job_title = dic['title']
        information.honour = dic['honour']
        information.remark = dic['comments']
        information.save()
        request.user.information = information
        request.user.save()
        return render(request, 'after_form.html')
    if request.method == "GET":
        resp = {}
        if information:
            resp = {'year_enroll': str(information.year_enroll), 'year_graduate': str(information.year_graduate)}
        return render(request, 'form.html', resp)


# @permission_required(perm="")
@login_required(login_url="user.login")
def get_excel(request):
    if request.user.is_superuser:
        fellows = SchoolFellow.objects.order_by('name')
        ws = Workbook(encoding="utf-8")
        w = ws.add_sheet(u"校友信息导出表")
        for i in fields:
            w.write(0, fields.index(i), i)
        date_format = XFStyle()
        date_format.num_format_str = 'yyyy-mm-dd'
        for i in range(len(fellows)):
            w.write(i + 1, 0, fellows[i].name)
            w.write(i + 1, 1, fellows[i].sex)
            w.write(i + 1, 2, fellows[i].tell)
            w.write(i + 1, 3, fellows[i].fixed_tell)
            w.write(i + 1, 4, fellows[i].email)
            w.write(i + 1, 5, fellows[i].department)
            w.write(i + 1, 6, fellows[i].school_class)
            w.write(i + 1, 7, fellows[i].education)
            w.write(i + 1, 8, fellows[i].year_system)
            # x = datetime.strftime(fellows[i].入学年份, '%Y-%m-%d')
            w.write(i + 1, 9, fellows[i].year_enroll, date_format)
            w.write(i + 1, 10, fellows[i].year_graduate, date_format)
            w.write(i + 1, 11, fellows[i].teacher)
            w.write(i + 1, 12, fellows[i].mentor)
            w.write(i + 1, 13, fellows[i].current_work_unit)
            w.write(i + 1, 14, fellows[i].address_work_unit)
            w.write(i + 1, 15, fellows[i].industry_category)
            w.write(i + 1, 16, fellows[i].unit_property)
            w.write(i + 1, 17, fellows[i].current_job_title)
            w.write(i + 1, 18, fellows[i].honour)
            w.write(i + 1, 19, fellows[i].remark)
        sio = BytesIO()
        ws.save(sio)
        sio.seek(0)
        res = HttpResponse(sio.getvalue(), content_type="application/vnd.ms-excel")
        sio.close()
        res['Content-Disposition'] = 'attachment;filename = school_fellow_information_export_table.xls'
        return res
    else:
        return HttpResponse("Permission denied.")
