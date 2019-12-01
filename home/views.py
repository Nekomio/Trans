from datetime import datetime

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# Create your views here.
from django.shortcuts import render, redirect

from home.models import Account, SchoolFellow


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        user = auth.user_logged_in
        if username and password:
            if Account.objects.filter(username=username):
                return HttpResponse("用户已存在")
            else:
                user = Account.objects.create_user(username=username, password=password)
                user.save()
                # 添加一些权限

                #
                return HttpResponse("注册成功")
        else:
            return HttpResponse("请正确输入")
    return render(request, "log.html")


def login(request):
    if request.method == "POST":
        print("has printed：post:", request.POST)
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        if Account.objects.filter(username=username):
            account = auth.authenticate(username=username, password=password)
            print("authenticated:", account)
            if account:
                if account.is_active:
                    auth.login(request, account)
                    return redirect(to="user.information")
                else:
                    return HttpResponse("the account is already active.")
            else:
                return HttpResponse("密码错误")
        else:
            return HttpResponse("用户不存在")
        # users = Account.objects.get_by_natural_key(username=username)
        # user = auth.authenticate(request,username=username,password=password)
        # print(user)
        # print(users)
    else:
        print("has printed GET:", request.GET)
        return render(request, "log.html")


@login_required(login_url='user.login')
def pass_reset(request):
    return HttpResponse("this is password reset.")


@login_required(login_url='user.login')
def logout(request):
    auth.logout(request)
    return redirect(to="user.logout")


# 'name': ['sa', 'sadlkfl;'], 'sex': ['1'], 'email': [''], 'yuanxi': [''], 'banji': [''], 'xueli': ['1'], 'xuezhi': [''], 'date1': [''], 'date2': [''], 'teacher': [''], 'workplace': [''], 'now-work': [''], 'industry-seletor': ['0'], 'workprop': ['0'], 'status': [''], 'prize': [''], 'byt': ['']}>
@login_required(login_url='user.login')
def information_filling(request):
    print("user:", request.user)
    print(request.user.information)
    if request.method == "POST":
        print(request.POST)
        dic = request.POST
        print('dic_name:', dic['name'])
        name = dic['name']
        tell = dic['name'][1]
        switch = {
            '1': "男",
            "2": "女",
        }
        sex = switch[dic['sex']]
        email = dic['email']
        yuanxi = dic['yuanxi']
        banji = dic['banji']
        switch = {
            "1": "本科生",
            "2": "硕士研究生",
            "3": "博士生",
        }
        xueli = switch[dic['xueli']]

        xuezhi = dic['xuezhi']
        date1 = datetime.strptime(dic['date1'], "%Y-%m-%d")
        date2 = datetime.strptime(dic['date2'], "%Y-%m-%d")
        try:
            teacher = dic['teacher']
        except:
            teacher = dic['professor']
        switch = {
            "1": "机关",
            "2": "事业单位",
            "3": "企业",
            "4": "其他",
        }

        workplace = dic['workplace']
        now_work = dic['now-work']
        industry_selector = dic['industry-seletor']
        try:
            workprop = dic['workprop']
        except:
            workprop = None
        title = dic['status']
        honor = dic['prize']
        comment = dic['byt']

        information = SchoolFellow(姓名=name, 性别=sex, 联系方式=tell, 电子邮箱=email, 院系=yuanxi, 班级=banji, 学历=xueli, 学制=xuezhi,
                                   入学年份=date1, 毕业年份=date2, 辅导员老师或印象最深刻的任课老师=teacher, 现工作单位=workplace, 工作单位地址=now_work,
                                   行业类别=switch[industry_selector], 单位性质=workprop, 现职务职称=title, 所获荣誉=honor, 备注=comment)

        print("information:", information, information.性别)
        information.save()
        request.user.information = information
        request.user.save()
        return HttpResponse("添加数据成功")
    else:
        information = request.user.information
        if information:
            print("information is", information.姓名, information.性别, information.联系方式, information.院系, information.班级,
                  information.学历, information.学制)
        return render(request, 'information_form.html', {'inf': information, 'name': information.姓名})
