from django import forms
# 要先导入forms模块
from captcha.fields import CaptchaField
# 注意需要提前导入from captcha.fields import CaptchaField，
# 然后就像写普通的form字段一样添加一个captcha字段就可以了

class UserForm(forms.Form):#所有的表单类都要继承forms.Form类
    username = forms.CharField(label='用户名',max_length=128,widget=forms.TextInput(attrs={'class': 'form-control'}))
    # 每个表单字段都有自己的字段类型比如CharField，它们分别对应一种HTML语言中<form>内的一个input元素。
    # 这一点和Django模型系统的设计非常相似。
    # label参数用于设置<label>标签
    # max_length限制字段输入的最大长度。它同时起到两个作用，
    # 一是在浏览器页面限制用户输入不可超过字符数，
    # 二是在后端服务器验证用户输入的长度也不可超过。


    password = forms.CharField(label='密码',max_length=256,widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码')
    # widget=forms.PasswordInput用于指定该字段在form表单里表现为<input type='password' />，
    # 也就是密码输入框






class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)
    # sex是一个select下拉框；
    captcha = CaptchaField(label='验证码')

