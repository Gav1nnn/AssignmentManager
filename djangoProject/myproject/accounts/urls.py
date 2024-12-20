# accounts/urls.py

from django.urls import path
from .views import HomeView, SignUpView, CustomLoginView, CustomLogoutView, ProfileView

app_name = 'accounts'  # 定义应用命名空间

urlpatterns = [
    path('', HomeView.as_view(), name='home'),  # 主页
    path('signup/', SignUpView.as_view(), name='signup'),  # 注册页面
    path('login/', CustomLoginView.as_view(), name='login'),  # 登录页面
    path('logout/', CustomLogoutView.as_view(), name='logout'),  # 登出页面
    path('profile/', ProfileView.as_view(), name='profile'),  # 个人资料页面
]