from django.db import models

class Note(models.Model):
	publish_time=models.DateTimeField(auto_now_add=True)
	update_time=models.DateTimeField(auto_now=True)
	caption=models.TextField()
	note=models.TextField()
