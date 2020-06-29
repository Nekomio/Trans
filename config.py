VERSION = 1
BACK_URL = 'back'
BACK_LOGIN_URL = BACK_URL + "/"
BACK_HOME_URL = BACK_URL + "/home"
MAIN_URL = 'user'
LOGOUT_URL = 'logout'
LOGIN_URL = 'login'
MAIN_LOGIN_URL = MAIN_URL + '/login'
MAIN_LOGOUT_URL = MAIN_URL + 'lo'
fields = [u'姓名',
          '性别',
          '移动电话/固定电话',
          '电子邮箱',
          '院系1',
          '班级1',
          '学历1',
          '学制1',
          '入学年份1',
          '毕业年份1',
          '印象最深刻的辅导员老师1',
          '印象最深刻的导师1',
          '院系2',
          '班级2',
          '学历2',
          '学制2',
          '入学年份2',
          '毕业年份2',
          '印象最深刻的辅导员老师2',
          '印象最深刻的导师2',
          '院系3',
          '班级3',
          '学历3',
          '学制3',
          '入学年份3',
          '毕业年份3',
          '印象最深刻的辅导员老师3',
          '印象最深刻的导师3',
          '现工作单位',
          '现工作单位地址',
          '行业类别',
          '单位性质',
          '现职务职称',
          '所获荣誉',
          '备注']

"""
1. 先在 form 里指定 metho：POST
2. form 里 标注 crf token
3. 在 loginveiw 里
"""
