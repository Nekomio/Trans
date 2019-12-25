//checkcode在后端验证!
//checkcode在后端验证!
let a=/^\w{6,}$/;
let b= /^([A-Za-z0-9_\-\.\u4e00-\u9fa5])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,8})$/;
let msg=document.getElementsByClassName("byr-form-msg")[0];
function che(e){
    let flag=b.test(e.value);
    if(flag){
        $(msg).hide();
        return true;
    }else{
        $(msg).show();
        msg.innerHTML="邮箱格式错误";
        return false;
    }
}
function chp(e) {
    let flag=a.test(e.value);
    if(flag){
        $(msg).hide();
        return true;
    }else{
        $(msg).show();
        msg.innerHTML="密码至少6位";
        return false;
    }
}
function functiona(){
    //后端先校验验证码:
    let checkcode=document.getElementById("byr-form-checkcode").value;
    //不行时阻止提交表单:
    return che()&&chp();
}