from allauth.account.adapter import DefaultAccountAdapter
from django import forms
from .utils import filter_users_by_email

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)
        data = form.cleaned_data
        user.member_email = data.get('email')
        user.account = data.get('account')
        user.display_name = data.get('display_name')
        if commit:
            user.save()
        return user

    def is_open_for_signup(self, request):
        return True

    def clean_username(self, username):
        return username

    def clean_email(self, email):
        # 이메일 중복 체크
        if filter_users_by_email(email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

    def send_mail(self, template_prefix, email, context):
        context['email'] = email
        msg = self.render_mail(template_prefix, email, context)
        msg.send()
