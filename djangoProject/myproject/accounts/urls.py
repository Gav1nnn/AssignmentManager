# accounts/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'  # 定义应用命名空间

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),

    # 使用 Django 自带的 LogoutView
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html', next_page='accounts:login'),
         name='logout'),

    path('student/home/', views.StudentHomeView.as_view(), name='student_home'),
    path('teacher/home/', views.TeacherHomeView.as_view(), name='teacher_home'),
    path('redirect-to-home/', views.RedirectToHome.as_view(), name='redirect_to_home'),
    path('error/', views.error_view, name='error'),  # 错误页面URL
]