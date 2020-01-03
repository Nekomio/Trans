import os
from io import BytesIO
from time import time

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
Obj_code.isTwist = False
Obj_code.line_count = 15


def get_path(img_name):
    check_code_dir = "check_code"
    src = "%s/%s" % (check_code_dir, img_name)
    return src, os.path.join(STATIC_ROOT, os.path.join(check_code_dir), img_name)


def register(request):
    print(request.POST)
    resp = {'error_msg': "", 'passcode_src': "", 'name': "", 'password': "", 'version': time()}
    session_key = str(hash(request.META['REMOTE_ADDR']))
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
        resp['checkpassword'] = request.POST['checkpassword']
        pass_code, pass_code_base64 = Obj_code.get_pass_code_base64()
        resp['passcode_src'] = pass_code_base64
        print(session_key, passcode)
        request.session[session_key] = passcode
        return render(request, 'register.html', resp)

    if request.method == "GET":
        pass_code, pass_code_base64 = Obj_code.get_pass_code_base64()
        resp['passcode_src'] = pass_code_base64
        print(session_key, pass_code)
        request.session[session_key] = pass_code
        return render(request, 'register.html', resp)


def login(request):
    resp = {'error_msg': "", 'passcode_src': "", 'name': "", 'password': "", 'version': time()}
    session_key = str(hash(request.META['REMOTE_ADDR']))
    if request.method == "POST":
        print("has printed：post:", request.POST)
        username = request.POST['username']
        password = request.POST['password']
        pass_code = request.POST['passcode']
        if request.session[session_key] != pass_code:
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
        pass_code, pass_code_base64 = Obj_code.get_pass_code_base64()
        print(session_key, pass_code)
        request.session[session_key] = pass_code
        resp['name'] = username
        resp['password'] = password
        resp['passcode_src'] = pass_code_base64
        return render(request, 'login.html', resp)
        # users = Account.objects.get_by_natural_key(username=username)
        # user = auth.authenticate(request,username=username,password=password)
        # print(user)
        # print(users)

    if request.method == "GET":
        # print("has printed GET:", request.GET)

        pass_code, pass_code_base64 = Obj_code.get_pass_code_base64()
        resp['passcode_src'] = pass_code_base64
        print(session_key, pass_code)
        request.session[session_key] = pass_code
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

        last_change_list = []
        if information.name != dic['name']:
            information.name = dic['name']
            last_change_list.append(fields[0])

        switch = {
            '1': "男",
            "2": "女",
        }
        if information.sex != switch[dic['sex']]:
            information.sex = switch[dic['sex']]
            last_change_list.append(fields[1])

        if information.tell != dic['tell']:
            information.tell = dic['tell']
            last_change_list.append(fields[2])

        if information.fixed_tell != dic['fixed_tell']:
            information.fixed_tell = dic['fixed_tell']
            last_change_list.append(fields[3])

        if information.email != dic['email']:
            information.email = dic['email']
            last_change_list.append(fields[4])

        if information.department != dic['department']:
            information.department = dic['department']
            last_change_list.append(fields[5])

        if information.school_class != dic['class']:
            information.school_class = dic['class']
            last_change_list.append(fields[6])

        switch1 = {
            "1": "本科生",
            "2": "硕士研究生",
            "3": "博士生",
        }
        if information.education != switch1[dic['education']]:
            information.education = switch1[dic['education']]
            last_change_list.append(fields[7])

        if information.year_system != dic['year']:
            information.year_system = dic['year']
            last_change_list.append(fields[8])

        year_enroll_choose_index = int(dic['startdate'])
        if year_enroll_choose_index != 0:
            if information.year_enroll != year_enroll_choose_index:
                information.year_enroll = year_enroll_choose_index
                last_change_list.append(fields[9])
        else:
            # information.year_enroll = None
            print(" has not choose the enroll year.")

        year_graduate_choose_index = int(dic['date2'])
        if year_graduate_choose_index != 0:
            if information.year_graduate != year_graduate_choose_index:
                information.year_graduate = year_graduate_choose_index
                last_change_list.append(fields[10])
        else:
            # information.year_graduate = None
            print("has not choose the graduate year.")

        try:
            if information.teacher != dic['teacher']:
                information.teacher = dic['teacher']
                last_change_list.append(fields[11])
        except:
            if information.mentor != dic['mentor']:
                information.mentor = dic['mentor']
                last_change_list.append(fields[12])
        if information.current_work_unit != dic['workplace']:
            information.current_work_unit = dic['workplace']
            last_change_list.append(fields[13])
        if information.address_work_unit != dic['address']:
            information.address_work_unit = dic['address']
            last_change_list.append(fields[14])

        switch2 = {
            "0": None,
            "1": "机关",
            "2": "事业单位",
            "3": "企业",
            "4": "其他",
        }
        if information.industry_category != switch2[dic['category']]:
            information.industry_category = switch2[dic['category']]
            last_change_list.append(fields[15])

        if dic['property'] != "0" and dic['property'] != '此处随行业类别变化而变化':
            if information.unit_property != dic['property']:
                information.unit_property = dic['property']
                last_change_list.append(fields[16])
        else:
            information.unit_property = None
            print("this user has not choose a correct unit_property")

        if information.current_job_title != dic['title']:
            information.current_job_title = dic['title']
            last_change_list.append(fields[17])
        if information.honour != dic['honour']:
            information.honour = dic['honour']
            last_change_list.append(fields[18])

        if information.remark != dic['comments']:
            information.remark = dic['comments']
            last_change_list.append(fields[19])

        string_changed_fields = ""
        for i in last_change_list:
            string_changed_fields += i + "/"
        information.last_changed_fields = string_changed_fields[:-1]
        print(information.last_changed_fields)
        information.save()
        request.user.information = information
        request.user.save()
        return render(request, 'after_form.html')
    if request.method == "GET":
        return render(request, 'form.html')


@permission_required(perm="home.view_schoolfellow", login_url="user.login", raise_exception=True)
@login_required(login_url="user.login")
def get_excel(request):
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
        w.write(i + 1, 9, fellows[i].year_enroll)
        w.write(i + 1, 10, fellows[i].year_graduate)
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
