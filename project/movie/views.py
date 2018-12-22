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
		# films[i]["t"]=hs+":"+ms+":"+ss
	return render(request, "movie/index.html", {"films":films})
	for i in range(0, len(d["films"])):
		films.append(d["films"][i])
		films[i]["plus"]=(d["films"][i]["pos"])*100/(d["films"][i]["neg"]+d["films"][i]["pos"])
		films[i]["minus"]=100-films[i]["plus"]
		t = d["films"][i]["time"]
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
		films[i]["t"]=hs+":"+ms+":"+ss
	return render(request, 'movie/index.html', {"films":films})

def findyear(request, year):
	films = []
	d = json.load(open('movie/templates/movie/films.json', encoding="utf8"))
	for i in range(0, len(d["films"])):
		if d["films"][i]["year"] == (int)(year):
			films.append(d["films"][i])
			films[len(films)-1]["plus"]=(d["films"][i]["pos"])*100/(d["films"][i]["neg"]+d["films"][i]["pos"])
			films[len(films)-1]["minus"]=100-films[len(films)-1]["plus"]
			t = d["films"][i]["time"]
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
			films[len(films)-1]["t"]=hs+":"+ms+":"+ss
	return render(request, 'movie/index.html', {"films":films, "year":year})