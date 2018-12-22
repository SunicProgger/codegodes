# -*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response, redirect 
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth import hashers
from django.template.context_processors import csrf
from pathlib import Path
from .models import Film
from django.utils.encoding import smart_str
import operator, time, json
# Create your views here.
def index(request):
	films = []
	# d = json.load(open('movie/templates/movie/films.json', encoding="utf8"))
	d = Film.objects.all()
	i = Film()
	for i in d:
		dn = {}
		dn["id"] = i.id
		dn["name"] = i.name
		dn["year"] = i.year
		dn["age"] = i.age
		dn["date"] = i.date
		dn["country"] = i.country
		dn["image"] = i.image.url
		dn["pos"] = i.pos
		dn["neg"] = i.neg 
		dn["prepos"] = (i.pos*100/(i.pos+i.neg))
		dn["preneg"] = 100-dn["prepos"]
		dn["categories"] = []
		cats = i.categories.split(' ')
		for j in cats:
			dn["categories"].append(j)
		dn["small_title"] = i.small_title
		dn["large_title"] = i.large_title
		dn["trailer"] = i.trailer
		t = i.time
		h = (int)(t/3600)
		m = (int)(t/60-h*60)
		s = (int)(t-h*3600-m*60)
		if h < 10:
			hs = "0"+(str)(h)
		else:
			hs = (str)(h)
		if m < 10:
			ms = "0"+(str)(m)
		else:
			ms = (str)(m)
		if s < 10:
			ss = "0"+(str)(s)
		else:
			ss = (str)(s)
		dn["time"] = hs+":"+ms+":"+ss
		films.append(dn)
	return render(request, "movie/index.html", {"films":films})

def findyear(request, year):
	films = []
	d = Film.objects.all()
	i = Film()
	for i in d:
		if i.year == (int)(year):
			dn = {}
			dn["id"] = i.id
			dn["name"] = i.name
			dn["year"] = i.year
			dn["age"] = i.age
			dn["date"] = i.date
			dn["country"] = i.country
			dn["image"] = i.image.url
			dn["pos"] = i.pos
			dn["neg"] = i.neg 
			dn["prepos"] = (i.pos*100/(i.pos+i.neg))
			dn["preneg"] = 100-dn["prepos"]
			dn["categories"] = []
			cats = i.categories.split(' ')
			for j in cats:
				dn["categories"].append(j)
			dn["small_title"] = i.small_title
			dn["large_title"] = i.large_title
			dn["trailer"] = i.trailer
			t = i.time
			h = (int)(t/3600)
			m = (int)(t/60-h*60)
			s = (int)(t-h*3600-m*60)
			if h < 10:
				hs = "0"+(str)(h)
			else:
				hs = (str)(h)
			if m < 10:
				ms = "0"+(str)(m)
			else:
				ms = (str)(m)
			if s < 10:
				ss = "0"+(str)(s)
			else:
				ss = (str)(s)
			dn["time"] = hs+":"+ms+":"+ss
			films.append(dn)
	return render(request, "movie/index.html", {"films":films, "year":year})

def findcat(request, category):
	films = []
	d = Film.objects.all()
	i = Film()
	for i in d:
		cats = i.categories.split(' ')
		if category in cats:
			dn = {}
			dn["id"] = i.id
			dn["name"] = i.name
			dn["year"] = i.year
			dn["age"] = i.age
			dn["date"] = i.date
			dn["country"] = i.country
			dn["image"] = i.image.url
			dn["pos"] = i.pos
			dn["neg"] = i.neg 
			dn["prepos"] = (i.pos*100/(i.pos+i.neg))
			dn["preneg"] = 100-dn["prepos"]
			dn["categories"] = []
			cats = i.categories.split(' ')
			for j in cats:
				dn["categories"].append(j)
			dn["small_title"] = i.small_title
			dn["large_title"] = i.large_title
			dn["trailer"] = i.trailer
			t = i.time
			h = (int)(t/3600)
			m = (int)(t/60-h*60)
			s = (int)(t-h*3600-m*60)
			if h < 10:
				hs = "0"+(str)(h)
			else:
				hs = (str)(h)
			if m < 10:
				ms = "0"+(str)(m)
			else:
				ms = (str)(m)
			if s < 10:
				ss = "0"+(str)(s)
			else:
				ss = (str)(s)
			dn["time"] = hs+":"+ms+":"+ss
			films.append(dn)
	return render(request, "movie/index.html", {"films":films, "category":category})

def findcountry(request, country):
	films = []
	d = Film.objects.all()
	i = Film()
	for i in d:
		if country != "others":
			if country == i.country:
				dn = {}
				dn["id"] = i.id
				dn["name"] = i.name
				dn["year"] = i.year
				dn["age"] = i.age
				dn["date"] = i.date
				dn["country"] = i.country
				dn["image"] = i.image.url
				dn["pos"] = i.pos
				dn["neg"] = i.neg 
				dn["prepos"] = (i.pos*100/(i.pos+i.neg))
				dn["preneg"] = 100-dn["prepos"]
				dn["categories"] = []
				cats = i.categories.split(' ')
				for j in cats:
					dn["categories"].append(j)
				dn["small_title"] = i.small_title
				dn["large_title"] = i.large_title
				dn["trailer"] = i.trailer
				t = i.time
				h = (int)(t/3600)
				m = (int)(t/60-h*60)
				s = (int)(t-h*3600-m*60)
				if h < 10:
					hs = "0"+(str)(h)
				else:
					hs = (str)(h)
				if m < 10:
					ms = "0"+(str)(m)
				else:
					ms = (str)(m)
				if s < 10:
					ss = "0"+(str)(s)
				else:
					ss = (str)(s)
				dn["time"] = hs+":"+ms+":"+ss
				films.append(dn)
		else:
			c = i.country
			if c != "USA" and c != "Russia" and c != "Germany" and c != "France":
				dn = {}
				dn["id"] = i.id
				dn["name"] = i.name
				dn["year"] = i.year
				dn["age"] = i.age
				dn["date"] = i.date
				dn["country"] = i.country
				dn["image"] = i.image.url
				dn["pos"] = i.pos
				dn["neg"] = i.neg 
				dn["prepos"] = (i.pos*100/(i.pos+i.neg))
				dn["preneg"] = 100-dn["prepos"]
				dn["categories"] = []
				cats = i.categories.split(' ')
				for j in cats:
					dn["categories"].append(j)
				dn["small_title"] = i.small_title
				dn["large_title"] = i.large_title
				dn["trailer"] = i.trailer
				t = i.time
				h = (int)(t/3600)
				m = (int)(t/60-h*60)
				s = (int)(t-h*3600-m*60)
				if h < 10:
					hs = "0"+(str)(h)
				else:
					hs = (str)(h)
				if m < 10:
					ms = "0"+(str)(m)
				else:
					ms = (str)(m)
				if s < 10:
					ss = "0"+(str)(s)
				else:
					ss = (str)(s)
				dn["time"] = hs+":"+ms+":"+ss
				films.append(dn)
	return render(request, "movie/index.html", {"films":films, "country":country})