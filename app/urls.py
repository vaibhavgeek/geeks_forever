from django.conf.urls import url,include
from django.contrib import admin
from . import views
urlpatterns = [
	url(r'^$',views.reader,name="reader"),
	url(r'questions/(?P<book_id>\d+)/$',views.questions, name= "questions")
]