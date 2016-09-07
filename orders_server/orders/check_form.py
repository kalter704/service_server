# -*- coding: utf-8 -*-

#from orders.models import UserProfile
from django.contrib.auth.models import User
from models import Categorie, Dish, UserProfile

def isEmptyField(temp):
	if temp == '':
		return True
	return False

def isEmptyThreeFields(username, email, password):
	if username == '':
		return True
	if email == '':
		return True
	if password == '':
		return True
	return False

def isEmptyFourFields(username, email, password, temp):
	if username == '':
		return True
	if email == '':
		return True
	if password == '':
		return True
	if temp == '':
		return True
	return False
	
def checkPassword(password, again_password):
	if password != again_password:
		return True
	return False
	
def isUserExist(username):
	is_exist = True
	try:
		u = User.objects.get(username = username)
	except:
		is_exist = False
	return  is_exist
	
def isCategorieExist(categorie):
	try:
		c = Categorie.objects.get(title = categorie)
	except:
		return False
	return True

def isDishExist(dish):
	try:
		d = Dish.objects.get(title = dish)
	except:
		return False
	return True

def isDishExist2(d_id, dish):
	try:
		d = Dish.objects.get(title = dish)
	except:
		return False
	if d_id == d.id:
		return False
	else:
		return True

def createProfileUser(username, email, password):
	u = User.objects.create_user(username, email, password)
	up = UserProfile(title = username, user = u)
	up.save()

def createCategorie(categorie, img):
	if img == None:
		img = 'Null'
	from datetime import datetime
	st = datetime.now().strftime("%y%m%d%H%M%S")
	c = Categorie(title = categorie, update_code = st, img = img)
	c.save()

def createDish(categorie, title, composition, price, weight, img):
	c = Categorie.objects.get(title = categorie)
	d = Dish(title = title, categorie = c, composition = composition, price = price, weight = weight, img = img)
	d.save()
	from datetime import datetime
	st = datetime.now().strftime("%y%m%d%H%M%S")
	c.update_code=st
	c.save()