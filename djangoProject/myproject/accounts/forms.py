# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from captcha.fields import CaptchaField
from .models import CustomUser  # 确保从当前应用导入自定义用户模型

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}),
        label=_("用户名")
    )
    email = forms.EmailField(
        max_length=254,
        help_text=_('请输入有效的电子邮件地址，这将是您接收通知的主要方式。'),
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'}),
        label=_("电子邮箱")
    )
    password1 = forms.CharField(
        label=_("密码"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        help_text=_('您的密码必须至少包含8个字符，且不能完全是数字。')
    )
    password2 = forms.CharField(
        label=_("确认密码"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        strip=False,
        help_text=_('请再次输入相同的密码以进行验证。')
    )
    user_type = forms.ChoiceField(
        choices=CustomUser.USER_TYPE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label=_("用户类型")
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'user_type', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                _("两个密码字段不匹配."),
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.user_type = self.cleaned_data["user_type"]
        if commit:
            user.set_password(self.cleaned_data["password1"])
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}),
        label=_("用户名")
    )
    password = forms.CharField(
        label=_("密码"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}),
    )
    captcha = CaptchaField(label=_('验证码'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                _("该账户已被禁用."),
                code='inactive',
            )
        if not (hasattr(user, 'is_student') and user.is_student() or hasattr(user, 'is_teacher') and user.is_teacher()):
            raise forms.ValidationError(
                _("您的用户类型不受支持."),
                code='invalid_user_type',
            )