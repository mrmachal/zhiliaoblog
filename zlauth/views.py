import string
import random
from django.shortcuts import render, reverse, redirect
from django.http.response import JsonResponse
from django.core.mail import send_mail
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model, login, logout

from .models import CaptchaModel
from .forms import RegisterForm, LoginForm

User = get_user_model()


# Create your views here.

@require_http_methods(['GET', 'POST'])
def zllogin(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                login(request, user)
                if not remember:
                    # 如果没有点击记住我，就要设置过期时间为零，即浏览器关闭后就过期
                    request.session.set_expiry(0)
                    # 如果点击了，就默认两周过期时间
                return redirect('/')
            else:
                print("邮箱或密码错误")
                # form.add_error('email', '邮箱或密码错误！')
                # return render(request, 'login.html', context={'form': form})
                return redirect(reverse('zlauth:login'))


def zllogout(request):
    logout(request)
    return redirect('/')


@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            User.objects.create_user(email=email, username=username, password=password)
            # 跳转到登录页面进行登录
            return redirect(reverse("zlauth:login"))
        else:
            print(form.errors)
            # 重新跳转到注册页面
            return redirect(reverse("zlauth:register"))
            # 也可以重新跳转到注册页面，将form作为参数传入，以显示错误信息
            # return render(request, 'register.html', context={'form': form})


def send_email_captcha(request):
    email = request.GET.get('email')
    if not email:
        return JsonResponse({"code": 400,
                             "message": "必须传递邮箱！"})
    #     生成验证码(取随机四位阿拉伯数字）
    captcha = "".join(random.sample(string.digits, 4))

    # 存储到数据库中
    CaptchaModel.objects.update_or_create(email=email, defaults={'captcha': captcha,
                                                                 'create_time': timezone.localtime()})
    send_mail("知了博客注册验证码", message=f"您好！\n您的注册验证码是：\n{captcha}",
              recipient_list=[email], from_email=None)
    return JsonResponse({
        "code": 200,
        "message": "邮箱发送成功!",
    })
