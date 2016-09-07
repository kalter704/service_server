# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from forms import ProfileUser, FormAddCategorie, FormAddDish
from check_form import isEmptyField, isEmptyThreeFields, isEmptyFourFields, checkPassword, isUserExist, createProfileUser, isCategorieExit, createCategorie, isDishExit, createDish
from models import Categorie, Dish
from pprint import pprint

# Create your views here.

def index(request):
	return render(request, 'main.html')

def allDishes(request):
	categorie_list = Categorie.objects.all()
	context = {
		'categorie_list': categorie_list
	}
	categorie = request.GET.get('categorie')
	if categorie != None:
		dish_list = Dish.objects.filter(categorie__title=categorie,)
		context.update({
			'categorie': categorie,
			'dish_list': dish_list
		})
	return render(request, 'allDishes.html', context)
	
def addCategorie(request):
	categorie_list = Categorie.objects.all()
	form = FormAddCategorie
	if request.POST:
		categorie = request.POST.get('title')
		img = request.FILES.get('img', None)
		is_empty_field = isEmptyField(categorie)
		if not is_empty_field:
			is_empty_field = isEmptyField(request.POST.get('img'))
		is_categorie_exist = isCategorieExit(categorie)
		
		#form.fields['title'] = categorie
		#form.img = img
		
		if is_categorie_exist or is_empty_field:
			context = {
				'categorie_list': categorie_list,
				'form': form,
				'is_categorie_exist': is_categorie_exist,
				'is_empty_field': is_empty_field
			}
		else:
			context = {
				'categorie_list': categorie_list,
				'form': form,
				'add_successful': True
			}
			createCategorie(categorie, img)
		return render(request, 'addCategorie.html', context)
	return render(request, 'addCategorie.html', {'form': form, 'categorie_list': categorie_list})
	
def addDish(request):
	categories = Categorie.objects.all()
	choices = [('', '')]
	for cat in categories:
		choices.append([cat.title, cat.title])
	form = FormAddDish()
	form.fields['categorie'].choices = choices
	if request.POST:
		categorie = request.POST.get('categorie')
		title = request.POST.get('title')
		price = request.POST.get('price')
		img = request.POST.get('img')
		is_empty_field = isEmptyFourFields(categorie, title, price, img)
		if is_empty_field:
			context = {
				'form': form,
				'is_empty_field': is_empty_field
			}
			#return render(request, 'addDish.html', context)
		else:
			is_dish_exit = isDishExit(title) 
			if is_dish_exit:
				context = {
					'form': form,
					'is_dish_exit': is_dish_exit
				}
				#return render(request, 'addDish.html', context)
			else:
				context = {
					'form': form,
					'add_successful': True
				}
				weight = request.POST.get('weight')
				composition = request.POST.get('composition')
				img = request.FILES.get('img', None)
				#pprint('create dish')
				createDish(categorie, title, composition, price, weight, img)
		return render(request, 'addDish.html', context)
	return render(request, 'addDish.html', {'form': form})
	
def register(request):
	form = ProfileUser
	if request.POST:
		username = request.POST.get('username')
		email = request.POST.get('email')
		password = request.POST.get('password')
		again_password = request.POST.get('again_password')
		
		#form.fields['username'] = username
		#form.fields['email'] = email
		
		is_empty_field = False
		is_wrong_pass = False
		is_user_exist = False
		
		if isEmptyThreeFields(username, email, password):
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
