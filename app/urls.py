from django.conf.urls import url,include
from django.contrib import admin
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	url(r'^$',views.reader,name="reader"),
	url(r'questions/(?P<book_id>\d+)/$',views.questions, name= "questions"),
	url(r'download/(?P<book_id>\d+)/$' , views.download,name = "download" ),
	url(r'download/page/(?P<book_id>\d+)/(?P<page_no>\d+)/$' , views.page,name = "page" ),
	]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)