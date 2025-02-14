from django.views import generic
from django.utils.translation import gettext_lazy as _
from .forms import LoginForm , SignupForm 
from django.contrib.auth.views import LoginView, LogoutView 
from django.shortcuts import redirect




# ログイン処理
class Login(LoginView):
    template_name = 'account/login.html'
    form_class = LoginForm  # カスタムフォームを指定
    redirect_authenticated_user = True  # すでにログインしているユーザーをリダイレクト

# ログアウト
class Logout(LogoutView):
    # ログアウト後はログインページへ遷移
    next_page = '/'

# サインアップ
class Signup(generic.CreateView):
    form_class = SignupForm
    template_name = 'account/signup.html'
    def form_valid(self, form):
        user = form.save()  # UserCreationForm が set_password を自動適用
        # login(self.request, user)  # 自動ログイン
        return redirect('/')
  
