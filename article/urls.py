from django.conf.urls import url
from . import views
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
		url(r'^$',views.blog_list,name='index'),
		url(r'^detail/id=(?P<id>[0-9]+)$',views.detail,name='detail'),
		url(r'^about/$',views.about,name='about'),
		url(r'^archive/(?P<sort>[a-z]+)$',views.archive,name='archive'),
		url(r'^write/$',views.write.write,name='write'),
		url(r'^write/(?P<id>[0-9]+)$',views.write.write,name='edit'),
		url(r'^editorText$',views.write.editorText,name='editorText'),
		url(r'^editorPic$',views.write.save_editorPic,name='editorPic'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)