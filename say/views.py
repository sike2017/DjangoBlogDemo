from django.shortcuts import render
from django.http import HttpResponse
from .models import *
import json
from django.contrib.auth.hashers import make_password,check_password
import re

def register(request):
	if request.method=='GET':
		return render(request,'register.html')
	if request.method=='POST':
		dic=request.POST
		password=make_password(dic['psd'],None,'pbkdf2_sha256')
		if len(speaker.objects.filter(name=dic['username']))!=0:
			rdic={'success':0,'message':'username is already existed'}
			return HttpResponse(json.dumps(rdic))
		user=speaker.objects.create(name=dic['username'],ps=password)
		if 'email' in dic:
			user.email=dic['email']
		if 'git' in dic:
			user.git=dic['git']
		user.save()
		rdic={'success':1,'message':'register successfully'}
		return HttpResponse(json.dumps(rdic))
	rdic={'success':0,'message':'if you are looking this, that meaning you are access the url without GET or POST'}
	return HttpResponse(json.dumps(rdic))

def loginChecker(request):
	if request.method=='GET':
		return render(request,'login.html')
	if request.method=='POST':
		dic=request.POST
		if 'username' in dic:
			user=speaker.objects.filter(name=dic['username'])
			if len(user)==0:
				rdic={'success':0,'message':'username or password is wrong'}
				return HttpResponse(json.dumps(rdic),content_type='application/json')		
			if 'psd' in dic and len(dic['psd'])!=0:
				if check_password(dic['psd'],user[0].ps)==True:
					#为了避免服务位于内部环境中时显示内部转发者的ip
					if 'HTTP_X_FORWARDED_FOR' in request.META:
						ip=request.META['HTTP_X_FORWARED_FOR']
					else:
						ip=request.META['REMOTE_ADDR']
					if re.search(r'[0-9]+\.[0-9]+\.[0-9]+\.[0-9]',ip) is None:
						rdic={'success':0,'message':'username or password is wrong'}
						return HttpResponse(json.dumps(rdic),content_type='application/json')
					else:
						if len(logined.objects.filter(user=user[0]))==0:
							logined.objects.create(user=user[0],ip=ip)
							rdic={'success':1,'message':'sign in successfully'}
							return HttpResponse(json.dumps(rdic),content_type='application/json')
						else:
							for item in logined.objects.filter(user=user[0]):
								item.delete()
							logined.objects.create(user=user[0],ip=ip)
							rdic={'success':2,'message':'your account was already logined at another network, we kick it out, and you sign in successfully'}
							return HttpResponse(json.dumps(rdic),content_type='application/json')
				else:
					rdic={'success':0,'message':'username or password is wrong'}
					return HttpResponse(json.dumps(rdic),content_type='application/json')
			else:
				rdic={'success':0,'message':'username or password is wrong'}
				return HttpResponse(json.dumps(rdic),content_type='application/json')
	rdic={'success':0,'message':'if you are looking this, that meaning you are access the url without GET or POST'}
	return HttpResponse(json.dumps(rdic),content_type='application/json')