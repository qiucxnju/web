from django.db import models
from authority.models import User
import hashlib, datetime, os
import re
from mysite import settings
class File(models.Model):
	owner = models.ForeignKey(User) # owner id
	path = models.CharField(max_length = 100) # article path
	title = models.CharField(max_length = 20) # article title
	submit_date = models.DateTimeField()
	@staticmethod
	def try_save(data, file, user):
		exist = True
		name = ""
		m = re.search(r'(\.[^.]+)$', file.name)
		while exist:	
			name = hashlib.sha224( "%s%s%s" % (name, user.name, str(datetime.datetime.now() ) ) ).hexdigest()
			if m is not None:
				name += m.group(1)
			exist = os.path.isfile("%s%s" % (settings.FILE_DIR, name)) 
		dest = open("%s%s" % (settings.FILE_DIR, name), 'wb')
		for chunk in file.chunks():
			dest.write(chunk)
		dest.close()
		file = File(owner = user,
						path = name,
						title = data['title'],
						submit_date = datetime.datetime.now())
		file.save() 
		return name