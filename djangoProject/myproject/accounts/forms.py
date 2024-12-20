# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from captcha.fields import CaptchaField

CustomUser = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'autofocus': True}),
        label=_("用户名")  # 修改为中文标签
    )
    email = forms.EmailField(
        max_length=254,
        help_text=_('请输入有效的电子邮件地址，这将是您接收通知的主要方式。'),  # 修改为中文帮助文本
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
        label=_("电子邮箱")
    )
    password1 = forms.CharField(
        label=_("密码"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=_('您的密码必须至少包含8个字符，且不能完全是数字。')  # 修改为中文帮助文本
    )
    password2 = forms.CharField(
        label=_("确认密码"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_('请再次输入相同的密码以进行验证。')  # 修改为中文帮助文本
    )

    class Meta:
        model = CustomUser  # 使用自定义用户模型
        fields = ['username', 'email', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True}),
        label=_("用户名")
    )
    password = forms.CharField(
        label=_("密码"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )
    captcha = CaptchaField(label='验证码')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # 移除 request 参数
        super().__init__(*args, **kwargs)

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                _("该账户已被禁用."),
                code='inactive',
            )