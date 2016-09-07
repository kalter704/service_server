# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from forms import ProfileUser, FormAddCategorie, FormAddDish, FormChangeDish
from check_form import isEmptyField, isEmptyThreeFields, isEmptyFourFields, checkPassword, isUserExist, createProfileUser, isCategorieExist, createCategorie, isDishExist, createDish, isDishExist2
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
		dish_list = Dish.objects.filter(categorie__title=categorie)
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
		is_categorie_exist = isCategorieExist(categorie)
		
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
			is_dish_exit = isDishExist(title) 
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
	
def changeDish(request):
	reqDish = request.GET.get('dish')
	if reqDish != None:
		form = FormChangeDish()
		categories = Categorie.objects.all()
		choices = [('','')]
		for cat in categories:
			choices.append([cat.title, cat.title])
		form.fields['categorie'].choices = choices

		dish = Dish.objects.get(title = reqDish)

		form.fields['prevTitle'].initial = dish.title
		form.fields['title'].initial = dish.title
		#form.fields['categorie'].selected = dish.categorie
		form.fields['composition'].initial = dish.composition
		form.fields['weight'].initial = dish.weight
		form.fields['price'].initial = dish.price

		context = {
			'form': form,
			'img': dish.img,
			'categorie': dish.categorie.title
		}
		return render(request, 'changeDish.html', context)
	else:
		if request.POST:
			prevTitle = request.POST.get('prevTitle')
			dish = Dish.objects.get(title = prevTitle)

			categorie = request.POST.get('categorie')
			title = request.POST.get('title')
			price = request.POST.get('price')
			weight = request.POST.get('weight')
			composition = request.POST.get('composition')
			img = request.POST.get('img')

			form = FormChangeDish()
			categories = Categorie.objects.all()
			choices = [('','')]
			for cat in categories:
				choices.append([cat.title, cat.title])
			form.fields['categorie'].choices = choices

			form.fields['prevTitle'].initial = dish.title
			form.fields['title'].initial = title
			#form.fields['categorie'].selected = dish.categorie
			form.fields['composition'].initial = composition
			form.fields['weight'].initial = weight
			form.fields['price'].initial = price

			is_empty_field = isEmptyThreeFields(categorie, title, price)
			if is_empty_field:
				context = {
					'form': form,
					'is_empty_field': is_empty_field,
					'img': dish.img,
					'categorie': categorie
				}
			else:
				is_dish_exit = isDishExist2(dish.id, title) 
				if is_dish_exit:
					context = {
						'form': form,
						'is_dish_exit': is_dish_exit,
						'img': dish.img,
						'categorie': categorie
					}
				else:
					dish.title = title
					dish.composition = composition
					dish.price = price
					dish.weight = weight
					if img != '':
						dish.img = request.FILES.get('img', None)
					c = Categorie.objects.get(title = categorie)
					dish.categorie = c
					dish.save()
					from datetime import datetime
					st = datetime.now().strftime("%y%m%d%H%M%S")
					c.update_code=st
					c.save()
					context = {
						'form': form,
						'add_successful': True,
						'img': dish.img,
						'categorie': categorie
					}
					form.fields['prevTitle'].initial = dish.title
			return render(request, 'changeDish.html', context)
		else:
			return redirect('/alldishes/')

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
