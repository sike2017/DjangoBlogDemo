from django.shortcuts import render
from .models import Tag,Classification,Author,Article,editorPic
from django.template import RequestContext
from django.http import Http404,HttpResponse
from django.forms import ModelForm
import datetime
import json 
from django.conf import settings
from django import forms
from django.utils.datastructures import MultiValueDictKeyError
from bs4 import BeautifulSoup
import re
from django.db import models

def blog_list(request):
	blogs=Article.objects.all().order_by('-publish_time')
	blog_b=blogs
	for blog in blog_b:
		soup=BeautifulSoup(blog.content,'html.parser')
		blog.content=soup.get_text()[:100]
	return render(request,'index.html',{"blogs":blog_b})

def detail(request, id):
	try:
		article=Article.objects.get(id=int(id))
	except:
		return render(request,'404.html')
	return render(request,'detail.html',{"article":article})

def about(request):
	return render(request,'about.html')

def archive(request,sort):
	articles=Article.objects.order_by("publish_time")
	if len(articles)==0:
		return render(request,'archive.html')
	articles=list(articles)
	rlist=[]
	i=0
	nowYear=articles[i].publish_time.year
	rlist=[[nowYear,[articles[i]]]]
	i=1
	yearNumber=0
	while i<len(articles):
		if(articles[i].publish_time.year!=nowYear):
			nowYear=articles[i].publish_time.year
			rlist.append([nowYear,[articles[i]]])
			i=i+1
			yearNumber=yearNumber+1
		else:
			rlist[yearNumber][1].append(articles[i])
			i=i+1
	# for litem in rlist:
	# 	litem[1]=tuple(litem[1])
	# i=0
	# while i<yearNumber:
	# 	rlist[i]=tuple(rlist[i])
	# rlist=tuple(rlist)
	return render(request,'archive.html',{'rlist':rlist})

# class write:
# 	class uploadForm(ModelForm):
# 		model=editorPic.image
# 	def write(request):
# 		return render(request,'write.html')
# 	def editorPic(request):
#          #         #  上传的后台只需要返回一个 JSON 数据，结构如下：
#          #  {
#          #     success : 0 | 1,           // 0 表示上传失败，1 表示上传成功
#          #     message : "提示的信息，上传成功或上传失败及错误信息等。",
#          #     url     : "图片地址"        // 上传成功时才返回
#          #  }
#          if request.method=='POST':
#          	if request.FILES.multiple_chunks(chunk_size=None):
#          		form=uploadForm(request.POST, request.FILES)
#          		if form.is_valid():
#          			form.save()
#          			rdic={'success':1,'message':1,'url':"%s/%s" %(settings.MEDIA_ROOT,editorPic.image)}
#          			return HttpResponse(json.dumps(rdic),content_type='application/json')
#          		else:
#          			form=uploadForm()
#          			pic_path=settings.MEDIA_ROOT+'/'+editorPic.image
#          			rdic={'success':0,'message':0}
#          			return HttpResponse(json.dumps(rdic),content_type='application/json')
#          else:
#          	rdic={'success':0,'message':0}
#          	return HttpResponse(json.dumps(rdic),content_type='application/json')

class write:
	class editorPicForm(ModelForm):
		class Meta:
			model=editorPic
			fields=['name','image']
	def save_editorPic(request):
		if request.method=='POST':
			if 'editormd-image-file' in request.FILES.keys():
				form=write.editorPicForm({'name':request.FILES['editormd-image-file'].name},{'image':request.FILES['editormd-image-file']})
			else:
				form=write.editorPicForm(request.POST,request.FILES)
			if form.is_valid():
				image=form.save()
				rdic={'success':1,'message':'upload successed','url':image.image.url}
				return HttpResponse(json.dumps(rdic),content_type='application/json')
			else:
				rdic={'success':0,'message':form.errors}
				return HttpResponse(json.dumps(rdic),content_type='application/json')
		else:
			rdic={'message':'hello there, if you are looking this, you should use a wrong method to visit this url, you should use POST to visit this url'}
			return HttpResponse(json.dumps(rdic),content_type='application/json')
	def editorText(request):
		def existOrCreate(item,iname):
			if len(item.objects.filter(name=iname))==0:
				item.objects.create(name=iname)
			return item.objects.get(name=iname)
		def content_decode(soup):
			try:
				if soup.body is None:
					s=str(soup)
				else:
					s=str(soup.body)
				info=re.search(r'^<h(?P<n>[0-6]).*>.*</h(?P=n)>\s*',s)
				caption=s[info.span()[0]:info.span()[1]]
				captionSoup=BeautifulSoup(caption,"html.parser")
				caption=captionSoup.get_text()
				content=s[info.span()[1]:]
				return (caption,content)
			except:
				return str(soup)
		if request.method=='POST':
			dic=request.POST
			if dic['pd']!=r'123456':
				rdic={'messsage':'pd error, refuse to update page'}
				return HttpResponse(json.dumps(rdic))
			if 'id' in dic:
				id=dic['id']
				if len(Article.objects.filter(id=id))==0:
					rdic={'success':0,'message':'article id does not exist'}
					return HttpResponse(json.dumps(rdic))
				else:
					art=Article.objects.get(id=id)
					soup=BeautifulSoup(dic['content'],'html.parser')
					cc=content_decode(soup)
					if not 'caption' in dic:
						caption=cc[0]
						if art.content!=cc[1]:
							art.content=cc[1]
					else:
						caption=dic['caption']
						if art.content!=dic['content']:
							art.content=dic['content']
					if art.caption!=caption:
						art.caption=caption
					if art.markdown_content!=dic['markdown_content']:
						art.markdown_content=dic['markdown_content']
					if str(art.classification)!=dic['classification']:
						art.classification=dic['classification']
					if 'subcaption' in dic:
						if len(art.subcaption)!=0:
							if dic['subcaption']!=art.subcaption:
								art.subcaption=dic['subcaption']
						else:
							art.subcaption=dic['subcaption']
					try:
						btags=[]
						for tag in art.tags.all():
							btags.append(tag.name)
						tags=dic.getlist('tags')
						for tag in tags:
							if not tag in btags:
								art.tags.add(existOrCreate(tag))
						for btag in btags:
							if not btag in tags:
								art.tags.filter(name=btag).delete()
						art.save()
						rdic={'success':1,'message':'update done'}
						return HttpResponse(json.dumps(rdic))
					except:
						rdic={'success':1,'message':'upload error'}
						return HttpResponse(json.dumps(rdic))
			soup=BeautifulSoup(dic['content'],'html.parser')
			cc=content_decode(soup)
			decoded_content=cc[1]
			if not 'caption' in dic:
				caption=cc[0]
			else:
				caption=dic['caption']
				decoded_content=dic['content']
			art=Article.objects.create(caption=caption,author=Author.objects.get(name=dic['author']),content=decoded_content,markdown_content=dic['markdown_content'],classification=existOrCreate(Classification,dic['classification']))
			# print(dic['tags'])
			# return HttpResponse('done')
			try:
				tags=dic.getlist('tags')
				for tag in tags:
					art.tags.add(existOrCreate(Tag,tag))
			except MultiValueDictKeyError:
				pass
			if 'subcaption' in dic.keys():
				art.subcaption=dic['subcaption']	
			art.save()
			rdic={'success':1,'message':'upload done','id':art.id}
			return HttpResponse(json.dumps(rdic),content_type='application/json')	
		else:
			rdic={'message':'hello there, if you are looking this, you should use a wrong method to visit this url, you should use POST to visit this url'}
			return HttpResponse(json.dumps(rdic),content_type='application/json')	
	def write(request,id=None):
		if id is None:
			rlist=['',-1]
			return render(request,'write.html',{'list':rlist})
		else:
			try:
				id=int(id)
				art=Article.objects.get(id=id)
				rlist=[art.markdown_content]
				rlist.append(id)
				return render(request,'write.html',{'list':rlist})
			except:
				return render(request,'404.html')
