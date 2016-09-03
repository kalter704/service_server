# -*- coding: utf-8 -*-
from orders.models import UserProfile
from django.contrib.auth.models import User
from models import Categorie

def isEmptyField(temp):
	if temp == '':
		return True
	return False

def isEmptyFields(username, email, password):
	if username == '':
		return True
	if email == '':
		return True
	if password == '':
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
	
def createProfileUser(username, email, password):
	u = User.objects.create_user(username, email, password)
	up = UserProfile(title = username, user = u)
	up.save()
	
def isCategorieExit(categorie):
	try:
		c = Categorie.objects.get(title = categorie)
	except:
		return False
	return True

def createCategorie(categorie, img):
	if img == None:
		img = 'Null'
	from datetime import datetime
	st = datetime.now().strftime("%y%m%d%H%M%S")
	c = Categorie(title = categorie, update_code = st, img = img)
	c.save()
