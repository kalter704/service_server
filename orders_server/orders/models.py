from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Categorie(models.Model):
	title = models.CharField(max_length = 25)
	update_code = models.CharField(max_length = 15)
	img = models.ImageField(upload_to = 'pic/', null = True)
	
class Dish(models.Model):
	title = models.CharField(max_length = 25)
	categorie = models.ForeignKey(Categorie)
	composition = models.TextField()
	price = models.IntegerField()
	weight = models.IntegerField()
	img = models.ImageField(upload_to = 'pic/', null = True)

#class Ingredient(models.Model):
#	title = models.CharField(max_length = 25)
#	dish = models.ManyToManyField(Dish)
#	img = models.ImageField(upload_to = 'pic/', null = True)
	
class Stock(models.Model):
	title = models.CharField(max_length = 50)
	text = models.TextField()
	stock_type = models.IntegerField()
	dish = models.ManyToManyField(Dish)
	img = models.ImageField(upload_to = 'pic/', null = True)
	
class UserProfile(models.Model):
	title = models.CharField(max_length = 20, default = '')	
	user = models.OneToOneField(User, related_name='profile')
	user_type = models.IntegerField(default = 0)
	
