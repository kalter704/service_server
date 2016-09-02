# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from forms import ProfileUser, FormAddCategorie
from check_form import isEmptyField, isEmptyFields, checkPassword, isUserExist, createProfileUser, isCategorieExit

# Create your views here.

def index(request):
	return render(request, 'main.html')

def allDishes(request):
	return HttpResponse("Hello, world. addDishes")
	
def addCategorie(request):
	form = FormAddCategorie
	if request.POST:
		categorie = request.POST.get('title')
		img = request.POST.get('img')
		is_empty_field = isEmptyField(categorie)
		if not is_empty_field:
			is_empty_field = isEmptyField(img)
		is_categorie_exist = isCategorieExit(categorie)
		if is_categorie_exist or is_empty_field:
			context = {
				'form': form,
				'is_categorie_exist': is_categorie_exist,
				'is_empty_field': is_empty_field
			}
		else:
			context = {
				'form': form,
				'add_successful': True
			}
			#
			# Функция добавления в БД
			#
		return render(request, 'addCategorie.html', context)
	return render(request, 'addCategorie.html', {'form': form})
	
def addDish(request):
	return HttpResponse("Hello, world. addDish")
	
def register(request):
	form = ProfileUser
	if request.POST:
		username = request.POST.get('username')
		email = request.POST.get('email')
		password = request.POST.get('password')
		again_password = request.POST.get('again_password')
		
		#form.fields['username'].initial = username
		#form.fields['email'].initial = email
		
		is_empty_field = False
		is_wrong_pass = False
		is_user_exist = False
		
		if isEmptyFields(username, email, password):
			is_empty_field = True
		if checkPassword(password, again_password):
			is_wrong_pass = True
		if isUserExist(username):
			is_user_exist = True
			
		if is_empty_field or is_wrong_pass or is_user_exist:
			context = {
				'form': form,
				'username': username,
				'email': email,
				'is_empty_field': is_empty_field,
				'is_wrong_pass': is_wrong_pass,
				'is_user_exist': is_user_exist
			}
			return render(request, 'register.html', context)
		else:
			createProfileUser(username, email, password)
			return redirect('/')
			
	return render(request, 'register.html', {'form': form})	
