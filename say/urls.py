from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^register/$',views.register),
	url(r'^register/registData/',views.register),
	url(r'^login/$',views.loginChecker),
	url(r'^login/loginData/',views.loginChecker),
]