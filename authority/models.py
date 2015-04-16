from django.db import models
from datetime import datetime, date, time
import hashlib
import json
# Create your models here.
class User(models.Model):
	name = models.CharField(max_length = 20) # the unique user handle
	password = models.CharField(max_length = 20) # the digested password
	realname = models.CharField(max_length = 10) # real name
	email = models.CharField(max_length = 50) # email address
	access_level = models.IntegerField() # access power
	# 1 means root, 1000 means guest
	@staticmethod
	def try_save(data):
		fetch = User.objects.filter(name = data['name'])

		if (len(fetch) > 0):
			return (False, 'User already existed.')

		if (len(data['name']) < 3):
			return (False, 'User Id must longer than 3')

		if (len(data['password']) < 3):
			return (False, 'User Password must longer than 3')

		if data['password'] != data['password2']:
			return (False, 'Password not consistant!')

		level = len(User.objects.all())
		if level is not 0:
			level = 1000
		user = User(
			name = data['name'],
			password = User.digest(data['password']),
			realname = data['realname'],
			email = data['email'],
			access_level = level)
		user.save()
		return (True, user)

	@staticmethod
	def digest(code):
		return hashlib.md5(code).hexdigest()[:20]

	@staticmethod
	def authenticate(data):
		name = data['name']
		password = data['password']
		found = User.objects.filter(name = name)
		if len(found) == 0:
			return (None, 'User not defined')
		elif found[0].password != User.digest(password):
			return (None, 'Password doesnot match')
		else:
			return (found[0], 'OK')

	@staticmethod
	def get_access_level(uid):
		result = User.objects.filter(id = uid)
		if len(result) == 0:
			return 10000
		else:
			return result[0].access_level

	@staticmethod
	def get_user_session(session):
		if 'id' in session:
			users = User.objects.filter(name = session['id'])
		else: users = []

		if len(users) > 0: 
			user = users[0]
		else: 
			user = None
		return user