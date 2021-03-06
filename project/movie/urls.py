# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
	url(r'^$', views.index, name="index"),
	url(r'login/', views.login, name="login"),
	url(r'register/', views.reg, name="register"),
	url(r'logout/', views.logout, name="logout"),
	url(r'^(?P<film>[0-9]+)/$', views.getfilm),
	url(r'y(?P<year>[0-9]+)/$', views.findyear),
	url(r'category_(?P<category>[\w-]+)/$', views.findcat),
	url(r'country_(?P<country>[\w-]+)/$', views.findcountry),
]