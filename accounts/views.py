from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.views import  LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from isu.models import Video, Comment
# from django.contrib.
# Create your views here.


class LoginPageView(LoginView): #로그인뷰는 accounts:profile을 자동으로 부른다
    template_name = 'form.html'


class LogoutPageView(LogoutView):#Not Found: /accounts/logout/form.html
    next_page = settings.LOGIN_URL 

class SignupView(CreateView):
    template_name = 'form.html'
    form_class = UserCreationForm
    success_url = settings.LOGIN_URL # accounts/login/

@login_required
def profile(request):
    myList = Video.objects.filter(author=request.user)
    context= {
        'name':request.user.username,
        'myList':myList,
        }

    return render(request, 'accounts/profile.html',context)