from django.db import models

class speaker(models.Model):
	name=models.CharField(max_length=50,unique=True)
	ps=models.CharField(max_length=300)
	email=models.EmailField(blank=True)
	git=models.URLField(blank=True)
	head=models.ImageField(upload_to='user')

	def __str__(self):
		return "%s"%(self.name)

	def __unicode__(self):
		return u"%s"%(self.name)

class say(models.Model):
	publish_time=models.DateTimeField(auto_now_add=True)
	editor=models.ForeignKey(speaker,related_name='sender',default='')
	write=models.TextField()
	say_to=models.ManyToManyField(speaker,blank=True,related_name='reciver')

	def __str__(self):
		return "%s"%(self.editor)

	def __unicode__(self):
		return u"%s"%(self.editor)

class logined(models.Model):
	user=models.ForeignKey(speaker)
	ip=models.CharField(max_length=50)