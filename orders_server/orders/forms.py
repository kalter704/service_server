# -*- coding: utf-8 -*-
from django import forms

class ProfileUser(forms.Form):
	username = forms.CharField(label='Логин', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	email = forms.EmailField(label='Mail', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	password = forms.CharField(label='Пароль', widget = forms.PasswordInput(attrs = {'class': 'form-control'}))
	again_password = forms.CharField(label='Повторите пароль', widget = forms.PasswordInput(attrs = {'class': 'form-control'}))
