collectForm = () => {
    fields = ['name', 'sex', 'phone',
        'email', 'yuanxi', 'banji', 'xueli1',
        'xuezhi1', 'startdate1', 'enddate1', 'teacher1','professor1',
        'workplace', 'now-work', 'industry-selector',
        'workprop', 'status', 'prize', 'byt'
    ]
    return Object.assign(...fields.map(k => ({
        [k]: getVal(k)
    })))
}
function getVal(id){
    console.log(id)
    return document.getElementById(id).value;
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
departmentVal = mkRequiredValidator('department1', '院系', x => x != "")
startVal = mkRequiredValidator('start1', '入学年份', x => x != "")
graduateVal = mkRequiredValidator('graduate1', '毕业年份', x => x != "")
workplaceVal = mkRequiredValidator('workplace1', '现工作单位', x => x != "")

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