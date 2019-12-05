collectForm = () => {
    fields = ['name', 'sex', 'phone', 'cellPhone',
        'email', 'department', 'class', 'education',
        'year', 'start', 'graduate', 'teacher',
        'workplace', 'address', 'category',
        'property', 'title', 'honour', 'comments'
    ]
    var getVal = field => document.getElementById(field).value
    return Object.assign(...fields.map(k => ({
        [k]: getVal(k)
    })))
}

function Either(isOk, val) {
    this.isOk = isOk
    this.val = val
}

Right = val => new Either(true, val)
Left = err => new Either(false, err)

isOk = m => m.isOk
flat = m => m.val

mkRequiredValidator = (field, alias, pred) =>
    form =>
    pred(form[field]) ?
    Right(form) :
    Left(alias + "为必填字段！")

sexVal = mkRequiredValidator('sex', '性别', x => x != "0")
nameVal = mkRequiredValidator('name', '姓名', x => x != "")
emailRVal = mkRequiredValidator('email', '电子邮箱', x => x != "")
departmentVal = mkRequiredValidator('department', '院系', x => x != "")
startVal = mkRequiredValidator('start', '入学年份', x => x != "")
graduateVal = mkRequiredValidator('graduate', '毕业年份', x => x != "")
workplaceVal = mkRequiredValidator('workplace', '现工作单位', x => x != "")

emailVal = form => (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(form['email'])) ? Right(form) : Left("电子邮箱无效！")
phoneOrCellPhoneVal = form => (form['phone'] == "" && form['cellPhone'] == "") ? Left("手机号码与固定电话至少填写一个！") : Right(form)


validators = [nameVal, sexVal, phoneOrCellPhoneVal,
    emailRVal, emailVal, departmentVal, startVal, graduateVal,
    workplaceVal
]

validateForm = (vs, form) => {
    const go = (mform, vs) => {
        if (!isOk(mform)) return mform
        if (vs.length == 0) return mform
        const [v, ...r] = vs
        return go(v(form), r)
    }
    return go(Right(form), vs)
}