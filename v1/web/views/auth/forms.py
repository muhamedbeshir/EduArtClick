from django import forms
from django.contrib.auth.models import User, Group


class LoginForm(forms.Form):
     username = forms.CharField(widget=forms.EmailInput(attrs={
         'class': 'form-control', 'placeholder': 'Email', 'autocomplete':'off'
     }), error_messages={'required': 'Please enter username !'}, label="", label_suffix="")
     password = forms.CharField(widget=forms.PasswordInput(attrs={
         'class': 'form-control', 'placeholder': 'Password', 'autocomplete':'off'
     }), error_messages={'required': 'Please enter  password !'}, label="", label_suffix="")



class StudentLoginForm(forms.Form):
     username = forms.CharField(widget=forms.TextInput(attrs={
         'class': 'form-control', 'placeholder': 'Username', 'autocomplete':'off'
     }), error_messages={'required': 'Please enter username !'}, label="", label_suffix="")
     password = forms.CharField(widget=forms.PasswordInput(attrs={
         'class': 'form-control', 'placeholder': 'Password', 'autocomplete':'off'
     }), error_messages={'required': 'Please enter  password !'}, label="", label_suffix="")


	