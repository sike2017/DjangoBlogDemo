from django.db import models

class Tag(models.Model):
	name=models.CharField(max_length=20)
	create_time=models.DateTimeField(auto_now_add=True)
	
	def __unicode__(self):
		return self.name
	def __str__(self):
		return self.name

class Classification(models.Model):
	name=models.CharField(max_length=20)

	def __unicode__(self):
		return self.name
	def __str__(self):
		return self.name

class Author(models.Model):
	name=models.CharField(max_length=30)
	email=models.EmailField(blank=True)
	website=models.URLField(blank=True)

	def __unicode__(self):
		return u'%s' %(self.name)
	def __str__(self):
		return '%s' %(self.name)

class Article(models.Model):
	caption=models.CharField(max_length=30)
	subcaption=models.CharField(max_length=50,blank=True)
	publish_time=models.DateTimeField(auto_now_add=True)
	update_time=models.DateTimeField(auto_now=True)
	author=models.ForeignKey(Author)
	classification=models.ForeignKey(Classification,blank=True)
	tags=models.ManyToManyField(Tag,blank=True)
	content=models.TextField()
	markdown_content=models.TextField(default="",blank=True)

	def __unicode__(self):
		return self.caption
	def __str__(self):
		return self.caption

class editorPic(models.Model):
	publish_time=models.DateTimeField(auto_now=True)
	update_time=models.DateTimeField(auto_now_add=True)
	name=models.CharField(max_length=50,blank=True)
	image=models.ImageField(upload_to='article')
