# -*- coding: utf-8 -*-
from django import forms

class ProfileUser(forms.Form):
	username = forms.CharField(label='Логин', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	email = forms.EmailField(label='Mail', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	password = forms.CharField(label='Пароль', widget = forms.PasswordInput(attrs = {'class': 'form-control'}))
	again_password = forms.CharField(label='Повторите пароль', widget = forms.PasswordInput(attrs = {'class': 'form-control'}))
	
class FormAddCategorie(forms.Form):
	title = forms.CharField(label='Название', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	img = forms.ImageField(label='Картинка', widget = forms.ClearableFileInput(attrs = {'class': 'form-control', 'onchange': 'readURL(this)'}))
	
class FormAddDish(forms.Form):
	#выбор категории 
	categorie = forms.ChoiceField(label = 'Категория', widget = forms.Select(attrs = {'class': 'form-control'}))
	title = forms.CharField(label = 'Название', widget = forms.TextInput(attrs = {'class': 'form-control'}))
	composition = forms.CharField(label = 'Состав', widget = forms.Textarea(attrs = {'class': 'form-control'}))
	weight = forms.IntegerField(label = 'Вес', widget = forms.NumberInput(attrs = {'class': 'form-control'}))
	price = forms.IntegerField(label = 'Цена', widget = forms.NumberInput(attrs = {'class': 'form-control'}))
	img = forms.ImageField(label = 'Картинка', widget = forms.ClearableFileInput(attrs = {'class': 'form-control', 'onchange': 'readURL(this)'}))
	
