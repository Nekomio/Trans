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
function chpa(e){
    // alert(e.value);
    let password=document.getElementsByName("password")[0];
    // alert(password.value);

    if(e.value!==password.value){
        $(msg).show();
        msg.innerHTML="两次密码输入不一致";
        return false;
    }else{
        $(msg).hide();
        return true;
    }
}
function functiona(){
    //后端校验验证码:
    let checkcode=document.getElementById("byr-form-checkcode").value;
    //不行时阻止提交:
    return che()&&chp()&&chpa();
}