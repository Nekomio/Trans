import os
from io import BytesIO

from django.contrib import auth
from django.contrib.auth.decorators import login_required, permission_required
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
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
    resp = {'error_msg': "", 'passcode_src': "", 'name': "", 'password': "", 'version': timezone.now()}
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
    resp = {'error_msg': "", 'passcode_src': "", 'name': "", 'password': "", 'version': timezone.now()}
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
        if information.sex_id != switch[dic['sex_id']]:
            information.sex_id = switch[dic['sex_id']]
            last_change_list.append(fields[1])

        if information.tell != dic['tell']:
            information.tell = dic['tell']
            last_change_list.append(fields[2])

        if information.email != dic['email']:
            information.email = dic['email']
            last_change_list.append(fields[3])

        if information.department1 != dic['department1']:
            information.department1 = dic['department1']
            last_change_list.append(fields[4])

        if information.school_class1 != dic['class1']:
            information.school_class1 = dic['class1']
            last_change_list.append(fields[5])

        switch1 = {
            "0": "None",
            "1": "本科生",
            "2": "硕士研究生",
            "3": "博士生",
        }
        if information.education1 != switch1[dic['education1']]:
            information.education1 = switch1[dic['education1']]
            last_change_list.append(fields[6])

        if information.year_system1 != dic['year1']:
            information.year_system1 = dic['year1']
            last_change_list.append(fields[7])

        year_enroll_choose_index1 = int(dic['startdate1'])
        if year_enroll_choose_index1 != 0:
            if information.year_enroll1 != year_enroll_choose_index1:
                information.year_enroll1 = year_enroll_choose_index1
                last_change_list.append(fields[8])
        else:
            # information.year_enroll1 = None
            print(" has not choose the enroll year.")

        year_graduate_choose_index1 = int(dic['date21'])
        if year_graduate_choose_index1 != 0:
            if information.year_graduate1 != year_graduate_choose_index1:
                information.year_graduate1 = year_graduate_choose_index1
                last_change_list.append(fields[9])
        else:
            # information.year_graduate1 = None
            print("has not choose the graduate year.")

        try:
            if information.teacher1 != dic['teacher1']:
                information.teacher1 = dic['teacher1']
                last_change_list.append(fields[10])
        except:
            if information.mentor1 != dic['mentor1']:
                information.mentor1 = dic['mentor1']
                last_change_list.append(fields[11])
        
        if information.department2 != dic['department2']:
            information.department2 = dic['department2']
            last_change_list.append(fields[12])

        if information.school_class2 != dic['class2']:
            information.school_class2 = dic['class2']
            last_change_list.append(fields[13])

        switch1 = {
            "0": "None",
            "1": "本科生",
            "2": "硕士研究生",
            "3": "博士生",
        }
        if information.education2 != switch1[dic['education2']]:
            information.education2 = switch1[dic['education2']]
            last_change_list.append(fields[14])

        if information.year_system2 != dic['year2']:
            information.year_system2 = dic['year2']
            last_change_list.append(fields[15])

        year_enroll_choose_index2 = int(dic['startdate2'])
        if year_enroll_choose_index2 != 0:
            if information.year_enroll2 != year_enroll_choose_index2:
                information.year_enroll2 = year_enroll_choose_index2
                last_change_list.append(fields[16])
        else:
            information.year_enroll2 = "0"
            print(" has not choose the enroll year.")

        year_graduate_choose_index2 = int(dic['date22'])
        if year_graduate_choose_index2 != 0:
            if information.year_graduate2 != year_graduate_choose_index2:
                information.year_graduate2 = year_graduate_choose_index2
                last_change_list.append(fields[17])
        else:
            information.year_graduate2 = "0"
            print("has not choose the graduate year.")

        try:
            if information.teacher2 != dic['teacher2']:
                information.teacher2 = dic['teacher2']
                last_change_list.append(fields[18])
        except:
            if information.mentor2 != dic['mentor2']:
                information.mentor2 = dic['mentor2']
                last_change_list.append(fields[19])
        
        if information.department3 != dic['department3']:
            information.department3 = dic['department3']
            last_change_list.append(fields[20])

        if information.school_class3 != dic['class3']:
            information.school_class3 = dic['class3']
            last_change_list.append(fields[21])

        switch1 = {
            "0": "None",
            "1": "本科生",
            "2": "硕士研究生",
            "3": "博士生",
        }
        if information.education3 != switch1[dic['education3']]:
            information.education3 = switch1[dic['education3']]
            last_change_list.append(fields[22])

        if information.year_system3 != dic['year3']:
            information.year_system3 = dic['year3']
            last_change_list.append(fields[23])

        year_enroll_choose_index3 = int(dic['startdate3'])
        if year_enroll_choose_index3 != 0:
            if information.year_enroll3 != year_enroll_choose_index3:
                information.year_enroll3 = year_enroll_choose_index3
                last_change_list.append(fields[24])
        else:
            information.year_enroll3 = "0"
            print(" has not choose the enroll year.")

        year_graduate_choose_index3 = int(dic['date23'])
        if year_graduate_choose_index3 != 0:
            if information.year_graduate3 != year_graduate_choose_index3:
                information.year_graduate3 = year_graduate_choose_index3
                last_change_list.append(fields[25])
        else:
            information.year_graduate3 = "0"
            print("has not choose the graduate year.")

        try:
            if information.teacher3 != dic['teacher3']:
                information.teacher3 = dic['teacher3']
                last_change_list.append(fields[26])
        except:
            if information.mentor3 != dic['mentor3']:
                information.mentor3 = dic['mentor3']
                last_change_list.append(fields[27])

        if information.current_work_unit != dic['workplace']:
            information.current_work_unit = dic['workplace']
            last_change_list.append(fields[28])
        if information.address_work_unit != dic['address']:
            information.address_work_unit = dic['address']
            last_change_list.append(fields[29])

        switch2 = {
            "0": None,
            "1": "机关",
            "2": "事业单位",
            "3": "企业",
            "4": "其他",
        }
        if information.industry_category != switch2[dic['category']]:
            information.industry_category = switch2[dic['category']]
            last_change_list.append(fields[30])

        if dic['property'] != "0" and dic['property'] != '此处随行业类别变化而变化':
            if information.unit_property != dic['property']:
                information.unit_property = dic['property']
                last_change_list.append(fields[31])
        else:
            information.unit_property = None
            print("this user has not choose a correct unit_property")

        if information.current_job_title != dic['title']:
            information.current_job_title = dic['title']
            last_change_list.append(fields[32])
        if information.honour != dic['honour']:
            information.honour = dic['honour']
            last_change_list.append(fields[33])

        if information.remark != dic['comments']:
            information.remark = dic['comments']
            last_change_list.append(fields[34])

        string_changed_fields = ""
        for i in last_change_list:
            string_changed_fields += i + "/"
        if last_change_list.__len__() != 0:
            information.last_changed_fields = string_changed_fields[:-1]
            information.last_submit = timezone.now()
            print("has changed the value of these fields:", information.last_changed_fields)
        information.save()
        request.user.information = information
        request.user.save()
        return render(request, 'after_form.html', {'version': timezone.now()})
    if request.method == "GET":
        return render(request, 'form_base.html', {'version': timezone.now()})


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
        if fellows[i].sex_id != 2:
            w.write(i + 1, 1, "男")
        else:
            w.write(i + 1, 1, "女")
        w.write(i + 1, 2, fellows[i].tell)
        w.write(i + 1, 3, fellows[i].email)
        w.write(i + 1, 4, fellows[i].department1)
        w.write(i + 1, 5, fellows[i].school_class1)
        w.write(i + 1, 6, fellows[i].education1)
        w.write(i + 1, 7, fellows[i].year_system1)
        w.write(i + 1, 8, fellows[i].year_enroll1)
        w.write(i + 1, 9, fellows[i].year_graduate1)
        w.write(i + 1, 10, fellows[i].teacher1)
        w.write(i + 1, 11, fellows[i].mentor1)
        
        if fellows[i].department2:
            w.write(i + 1, 12, fellows[i].department2)
        if fellows[i].school_class2:
            w.write(i + 1, 13, fellows[i].school_class2)
        if fellows[i].education2:
            w.write(i + 1, 14, fellows[i].education2)
        if fellows[i].year_system2:
            w.write(i + 1, 15, fellows[i].year_system2)
        if fellows[i].year_enroll2:
            w.write(i + 1, 16, fellows[i].year_enroll2)
        if fellows[i].year_graduate2:
            w.write(i + 1, 17, fellows[i].year_graduate2)
        if fellows[i].teacher2:
            w.write(i + 1, 18, fellows[i].teacher2)
        if fellows[i].mentor2:
            w.write(i + 1, 19, fellows[i].mentor2)

        if fellows[i].department3: 
            w.write(i + 1, 20, fellows[i].department3)
        if fellows[i].school_class3: 
            w.write(i + 1, 21, fellows[i].school_class3)
        if fellows[i].education3: 
            w.write(i + 1, 22, fellows[i].education3)
        if fellows[i].year_system3: 
            w.write(i + 1, 23, fellows[i].year_system3)
        if fellows[i].year_enroll3: 
            w.write(i + 1, 24, fellows[i].year_enroll3)
        if fellows[i].year_graduate3: 
            w.write(i + 1, 25, fellows[i].year_graduate3)
        if fellows[i].teacher3: 
            w.write(i + 1, 26, fellows[i].teacher3)
        if fellows[i].mentor3: 
            w.write(i + 1, 27, fellows[i].mentor3)

        w.write(i + 1, 28, fellows[i].current_work_unit)
        w.write(i + 1, 29, fellows[i].address_work_unit)
        w.write(i + 1, 30, fellows[i].industry_category)
        w.write(i + 1, 31, fellows[i].unit_property)
        w.write(i + 1, 32, fellows[i].current_job_title)
        w.write(i + 1, 33, fellows[i].honour)
        w.write(i + 1, 34, fellows[i].remark)
    w.col(2).width = 5000
    w.col(3).width = 6144
    w.col(4).width = 4000
    w.col(5).width = 3000
    w.col(10).width = 4000
    w.col(11).width = 4000
   
    w.col(12).width = 4000
    w.col(13).width = 3000
    w.col(18).width = 4000
    w.col(19).width = 4000

    w.col(20).width = 4000
    w.col(21).width = 3000
    w.col(26).width = 4000
    w.col(27).width = 4000

    w.col(28).width = 4000
    w.col(29).width = 4000
    w.col(30).width = 4000
    w.col(31).width = 4000
    w.col(32).width = 4000
    w.col(33).width = 4000
    w.col(34).width = 40000

    sio = BytesIO()
    ws.save(sio)
    sio.seek(0)
    res = HttpResponse(sio.getvalue(), content_type="application/vnd.ms-excel")
    sio.close()
    res['Content-Disposition'] = 'attachment;filename = school_fellow_information_export_table.xls'
    return res
