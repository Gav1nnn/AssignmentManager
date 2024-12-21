# accounts/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, RedirectView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model, login
from .forms import CustomUserCreationForm, CustomAuthenticationForm  # 使用自定义表单
from courses.models import Course
import logging

CustomUser = get_user_model()
logger = logging.getLogger(__name__)

class HomeView(TemplateView):
    template_name = 'accounts/home.html'


class SignUpView(CreateView):
    form_class = CustomUserCreationForm  # 使用你的自定义表单
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:home')  # 注册成功后重定向到主页或其他页面

    def get_initial(self):
        initial = super().get_initial()
        if self.request.method == 'GET':
            initial['user_type'] = self.request.GET.get('user_type', '')
            initial['username'] = self.request.GET.get('username', '')
            initial['email'] = self.request.GET.get('email', '')
            initial['password1'] = self.request.GET.get('password1', '')
            initial['password2'] = self.request.GET.get('password2', '')
            initial['invite_code'] = self.request.GET.get('invite_code', '')
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Determine whether to show invite code and captcha based on initial_user_type or POST data
        user_type = self.request.GET.get('user_type', '') or self.request.POST.get('user_type', '')
        context['show_invite_code'] = (user_type == 'teacher')
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)  # 自动登录新注册的用户
        return response


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = CustomAuthenticationForm  # 使用自定义的认证表单

    def get_success_url(self):
        if self.request.user.is_student():
            return reverse_lazy('accounts:student_home')
        elif self.request.user.is_teacher():
            return reverse_lazy('accounts:teacher_home')
        else:
            return reverse_lazy('accounts:home')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:home')  # 登出后重定向到主页

class StudentHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/student_home.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_student():
            return redirect('accounts:error')  # 或者返回一个错误页面
        return super().dispatch(request, *args, **kwargs)

class TeacherHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/teacher_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 获取当前用户教授的所有课程
        courses = Course.objects.filter(teacher=self.request.user)
        logger.info(f"Found {courses.count()} courses for user {self.request.user.username}")
        context['courses'] = courses
        return context

class RedirectToHome(RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated:
            if user.is_student():
                return reverse_lazy('accounts:student_home')
            elif user.is_teacher():
                return reverse_lazy('accounts:teacher_home')
        return reverse_lazy('accounts:home')

def error_view(request):
    return render(request, 'accounts/error.html', {'message': '您没有权限访问该页面，请联系管理员。'})