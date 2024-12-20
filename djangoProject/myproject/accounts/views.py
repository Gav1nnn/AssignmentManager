# accounts/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm, CustomAuthenticationForm  # 使用自定义表单
from django.contrib.auth import get_user_model, login as auth_login

CustomUser = get_user_model()

class HomeView(TemplateView):
    template_name = 'accounts/home.html'

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def protected_view(request):
    return render(request, 'accounts/protected.html')


class SignUpView(CreateView):
    form_class = CustomUserCreationForm  # 使用自定义的注册表单
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        auth_login(self.request, self.object)  # 自动登录新用户
        return response

    def get_success_url(self):
        return reverse_lazy('accounts:home')  # 使用命名空间前缀


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = CustomAuthenticationForm  # 使用自定义的认证表单
    next_page = reverse_lazy('accounts:profile')  # 确保使用命名空间前缀


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:home')  # 登出后重定向到主页，使用命名空间前缀


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user  # 将当前用户信息传递给模板
        return context