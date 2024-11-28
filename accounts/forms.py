from django import forms
from django.contrib.auth.models import User
from django.shortcuts import render

from accounts.models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput,
                               label='Password')

    password_2 = forms.CharField(widget=forms.PasswordInput,
                                label='Confirm Password')


    class Meta:
        model = User
        fields = ('username','first_name','email')

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password_2']:
            raise forms.ValidationError("Passwords don't match")
        return data['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth','photo']


