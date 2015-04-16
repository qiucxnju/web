from django.db import models
from datetime import datetime, date, time
import hashlib
import json
from authority.models import User

class Tag(models.Model):
	value = models.CharField(max_length = 20)

class Blog(models.Model):
	# for all the documentations!!
	title = models.CharField(max_length = 20) # article title
	date = models.DateField()
	path = models.CharField(max_length = 100) # article path
	content = models.TextField() # the wiki body
	edit_level = models.IntegerField() # the level need to edit this page
	view_level = models.IntegerField() # the level need to read this page
	owner = models.ForeignKey(User) # owner id
	tags = models.ManyToManyField(Tag)

	@staticmethod
	def get_blog_path(path):
		blogs = Blog.objects.filter(path = path)
		if len(blogs) > 0: blog = blogs[0]
		else: blog = None
		return blog
		
	@staticmethod
	def try_save(data, path, user, blog):
		if user is None:
			return (None, "please login first")
		if user.access_level > 1:
			return (None, "you have no authority to write blog")

		if blog is not None:
			if blog.owner != user:
				return (None, "you have no authority to modify this blog")
		if (data['show'] == 'true'):
			level = 1000
		else:
			level = user.access_level
		new_blog = Blog(
			title = data['title'],
			date = datetime.strptime (data['date'], '%Y-%m-%d'),
			path = path,
			content = data['content'],
			edit_level = user.access_level,
			view_level = level,
			owner = user,
			)

		tag_list = []
		for value in json.loads(data['tags']):
			tags = Tag.objects.filter(value = value)
			if len(tags) == 0:
				tag = Tag(value = value)
				tag.save()
			else: 
				tag = tags[0]
			tag_list.append(tag)
		new_blog.save()
		for tag in tag_list:
			new_blog.tags.add(tag)
		if blog is not None:
			blog.delete()