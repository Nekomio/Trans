BACK_URL = 'back'
BACK_LOGIN_URL = BACK_URL + "/"
BACK_HOME_URL = BACK_URL + "/home"
MAIN_URL = 'user'
LOGOUT_URL = 'logout'
LOGIN_URL = 'login'
MAIN_LOGIN_URL = MAIN_URL + '/login'
MAIN_LOGOUT_URL = MAIN_URL + 'lo'
FIELDS = ['姓名',
          '性别',
          '联系方式',
          '电子邮箱',
          '院系',
          '班级',
          '学历',
          '学制',
          '入学年份',
          '毕业年份',
          '辅导员老师或印象最深刻的任课老师',
          '现工作单位',
          '工作单位地址',
          '行业类别',
          '单位性质',
          '现职务职称',
          '所获荣誉',
          '备注', ]

"""
1. 先在 form 里指定 metho：POST
2. form 里 标注 crf token
3. 在 loginveiw 里
"""
