from django.shortcuts import render
from django.shortcuts import redirect
from .models import User
from login import form

import hashlib
import datetime

# Create your views here.




def hash_code(s,salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user,)
    return code
    # make_confirm_string()方法接收一个用户对象作为参数。
    # 首先利用datetime模块生成一个当前时间的字符串now，
    # 再调用我们前面编写的hash_code()方法以用户名为基础，now为‘盐’，
    # 生成一个独一无二的哈希值，再调用ConfirmString模型的create()方法，
    # 生成并保存一个确认码对象。最后返回这个哈希值。

def send_email(email, code):

    from django.core.mail import EmailMultiAlternatives

    subject = '欢迎您使用用户登录于注册系统！'

    text_content = '''感谢注册洪一夫的注册系统，该系统基于django开发，实现了注册，登录，数据保存，邮箱验证等功能！
                    ！'''

    html_content = '''
                    <p>感谢注册<a href="47.100.228.116:8000/index" target=blank>47.100.228.116:8000/index</a>
                    </p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为7天！</p>
                    '''

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()



def index(request):
    pass
    
    # print(request.session)
    # print(request.session['user_name'])
    return render(request,'login/index.html')




def login(request):

    # 通过下面的if语句，我们不允许重复登录：
    if request.session.get('is_login',None):
        
        # print(request.session)
        return redirect("/index/")


    # 每个视图函数都至少接收一个参数，并且是第一位置参数，该参数封装了当前请求的所有数据；
    # 通常将第一参数命名为request，当然也可以是别的；
    if request.method == 'POST':
        #request.method中封装了数据请求的方法，如果是“POST”（全大写），将执行if语句的内容，
        # 如果不是，直接返回最后的render()结果；
        # username = request.POST.get('username',None)
        # request.POST封装了所有POST请求中的数据，这是一个字典类型，可以通过get方法获取具体的值。
        # 类似get('username')中的键‘username’是HTML模板中表单的input元素里‘name’属性定义的值。
        # 所以在编写form表单的时候一定不能忘记添加name属性。
        # 
        # password = request.POST.get('password',None)

        login_form = form.UserForm(request.POST)
        message = "请检查填写内容!！"
        if login_form.is_valid():
            # 使用表单类自带的is_valid()方法一步完成数据验证工作；
            #验证全部通过
            # 其中验证图形码是否正确的工作都是在后台自动完成的，
            # 只需要使用is_valid()这个forms内置的验证方法就一起进行了，
            # 完全不需要在视图函数中添加任何的验证代码，非常方便快捷！
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            # 验证成功后可以从表单对象的cleaned_data数据字典中获取表单的具体值；
            try:
                user = User.objects.get(name=username)
                if not user.has_confirmed:
                    message = "该用户还未通过邮件确认！"
                    return render(request, 'login/login.html', locals())
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return render(request,'login/index.html',{'username':username})
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login/login.html', locals())
    login_form = form.UserForm()
    return render(request, 'login/login.html', locals())
    # 另外，这里使用了一个小技巧，Python内置了一个locals()函数，
    # 它返回当前所有的本地变量字典，我们可以偷懒的将这作为render函数的数据字典参数值，
    # 就不用费劲去构造一个形如{'message':message, 'login_form':login_form}的字典了。
    # 这样做的好处当然是大大方便了我们，
    # 但是同时也可能往模板传入了一些多余的变量数据，造成数据冗余降低效率。









    #     if username and password:
    #         #数据验证
    #         username = username.strip()
    #         #通过strip()方法，将用户名前后无效的空格剪除；
    #         print('1')
    #         try:
    #             user = User.objects.get(name=username)
    #             # models.User.objects.get(name=username)是Django提供的最常用的数据查询API，
    #             # 使用try异常机制，防止数据库查询失败的异常；
    #             print('2')
    #             #比较username是否存在于数据库中
    #         except:
    #             #不存在，返回登录页面
    #             message = '用户名不存在！'
    #             return render(request,'login/login.html',{'message':message})
            
    #         if user.password != password:
    #             message = '密码不正确！'
    #             return render(request,'login/login.html',{'message':message})
                
    #         else:
    #             return render(request,'login/index.html',{'username':username})



    #     print(username,password)
        
    #     return redirect('/index/')
    # return render(request,'login/login.html')

def register(request):
    if request.session.get('is_login',None):
        # print(request.session)
        return redirect("/index/")
    if request.method == "POST":
        register_form = form.RegisterForm(request.POST)
        
        message = "请检查填写的内容！"
        print('1')
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            print('1')
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'login/register.html', locals())
                same_email_user = User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login/register.html', locals())
                 # 当一切都OK的情况下，创建新用户
                print('2')
                new_user = User()
                new_user.name = username
                new_user.password = hash_code(password1)  # 使用加密密码
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                print('3')

                code = make_confirm_string(new_user)
                send_email(email, code)



                return redirect('/login/')  # 自动跳转到登录页面
    register_form = form.RegisterForm()
    return render(request,'login/register.html',locals())




def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()
    # ush()方法是比较安全的一种做法，而且一次性将session中的所有内容全部清空，确保不留后患。
    # 但也有不好的地方，那就是如果你在session中夹带了一点‘私货’，会被一并删除，这一点一定要注意。

    return redirect('/index/')#重定向 url
    #在顶部额外导入了redirect，用于logout后，页面重定向到‘index’首页；
    '''


    四个视图都返回一个render()调用，render方法接收request作为第一个参数，
    要渲染的页面为第二个参数，以及需要传递给页面的数据字典作为第三个参数（可以为空），
    表示根据请求的部分，以渲染的HTML页面为主体，使用模板语言将数据字典填入，
    然后返回给用户的浏览器。
    渲染的对象为login目录下的html文件，这是一种安全可靠的文件组织方式。
    '''


def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, 'login/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'login/confirm.html', locals())
