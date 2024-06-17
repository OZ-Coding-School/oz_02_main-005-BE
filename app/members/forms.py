from allauth.account.forms import LoginForm, SignupForm
from django import forms

class CustomLoginForm(LoginForm):
    login = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

class CustomSignupForm(SignupForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    account = forms.CharField(label='Account', widget=forms.TextInput(attrs={'placeholder': 'Account'}))
    display_name = forms.CharField(label='Display Name', widget=forms.TextInput(attrs={'placeholder': 'Display Name'}))

    def save(self, request):
        user = super().save(request)
        user.member_email = self.cleaned_data['email']
        user.account = self.cleaned_data['account']
        user.display_name = self.cleaned_data['display_name']
        user.save()
        return user
