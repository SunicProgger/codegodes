# -*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response, redirect 
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth import hashers
from django.template.context_processors import csrf
from pathlib import Path
from .models import Film, User
from django.utils.encoding import smart_str
import operator, time, json, hashlib
import datetime as date


'''class Block:

    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index

        self.timestamp = timestamp

        self.data = data

        self.previous_hash = previous_hash

        self.hash = self.hash_block()

    def hash_block(self):
        return hashlib.sha256(str(str(self.index) +

                   str(self.timestamp) +

                   str(self.data) +

                   str(self.previous_hash)).encode('utf-8')).hexdigest()'''


def index(request):
	films = []
	myfilms = []
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
		dn["cost"] = i.cost
		dn["prepos"] = (i.pos*100/(i.pos+i.neg))
		dn["preneg"] = 100-dn["prepos"]
		dn["categories"] = []
		dn["has"] = False
		if not request.user.is_anonymous:
			if request.user.data > "":
				myfilms = request.user.data.split(' ')
				for j in range(0, len(myfilms)):
					if i.id == (int)(myfilms[j]):
						dn["has"] = True;
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
	return render(request, "movie/index.html", {"films":films, "myfilms":myfilms})

def login(request):
	args = {}
	args.update(csrf(request))
	if request.POST:
		username = request.POST.get('login')
		password = request.POST.get('password')
		user = auth.authenticate(login = username, password = password)
		if user is not None:
			if user.is_active == True:
				auth.login(request, user)
				return redirect('/')
			else:
				return redirect('/')
		else:
			args['login_error'] = "no user"
			args['nologin'] = username
			args['nopass'] = password
			return render_to_response('movie/index.html', args)
	else:
		return render_to_response('movie/index.html', args)
def reg(request):
	args = {}
	args.update(csrf(request))
	if request.POST:
		films = []
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
			dn["cost"] = i.cost
			dn["prepos"] = (i.pos*100/(i.pos+i.neg))
			dn["preneg"] = 100-dn["prepos"]
			dn["categories"] = []
			dn["has"] = False
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
		args['films'] = films
		username = request.POST.get('reglogin')
		pass1 = request.POST.get('regpass1')
		pass2 = request.POST.get('regpass2')
		date = request.POST.get('regdate')
		snils = request.POST.get('snils')
		args['date'] = date
		args['snils'] = snils
		up = User.objects.all()
		k = 0;
		for i in up:
			if i.login == username:
				k += 1
		if k > 0:
			args['reg_error'] = "no user"
			return render_to_response('movie/index.html', args)
		if pass1 != pass2 or len(pass1) <= 8:
			args['reg_error'] = "bad pass"
			args['login'] = username
			return render_to_response('movie/index.html', args)
		u = User()
		u.login = username
		u.snils = snils
		u.date = date
		u.set_password(pass1)
		u.save()
		# db = json.load(open('movie/database.json', encoding='utf8'))
		with open('movie/database.json', mode='r', encoding='utf-8') as feedsjson:
			db = json.load(feedsjson)
		hash = db[len(db)-1]['hash'] 
		snils = request.post.get('snils') 
		status = "Moderation..."
		dict3 = {'snils':snils, 'status':status, 'hash':hash} 
		db.append(dict3)
		with open("movie/database.json", 'w') as file:
			json.dump(db, file, indent=2)
		user = auth.authenticate(login = username, password = pass1)
		auth.login(request, user)
	return redirect('/')
def logout(request):
	auth.logout(request)
	return redirect('/')
def findyear(request, year):
	films = []
	d = Film.objects.all()
	i = Film()
	if (int)(year) < 2015:
		for i in d:
			if i.year < 2015:
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
				dn["cost"] = i.cost
				dn["prepos"] = (i.pos*100/(i.pos+i.neg))
				dn["preneg"] = 100-dn["prepos"]
				dn["categories"] = []
				dn["has"] = False
				if request.user:
					if request.user.data > "":
						myfilms = request.user.data.split(' ')
						for j in range(0, len(myfilms)):
							if i.id == (int)(myfilms[j]):
								dn["has"] = True;
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
				dn["cost"] = i.cost
				dn["prepos"] = (i.pos*100/(i.pos+i.neg))
				dn["preneg"] = 100-dn["prepos"]
				dn["categories"] = []
				dn["has"] = False
				if request.user:
					if request.user.data > "":
						myfilms = request.user.data.split(' ')
						for j in range(0, len(myfilms)):
							if i.id == (int)(myfilms[j]):
								dn["has"] = True;
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
			dn["cost"] = i.cost
			dn["prepos"] = (i.pos*100/(i.pos+i.neg))
			dn["preneg"] = 100-dn["prepos"]
			dn["categories"] = []
			dn["has"] = False
			if request.user:
				if request.user.data > "":
					myfilms = request.user.data.split(' ')
					for j in range(0, len(myfilms)):
						if i.id == (int)(myfilms[j]):
							dn["has"] = True;
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
				dn["cost"] = i.cost
				dn["prepos"] = (i.pos*100/(i.pos+i.neg))
				dn["preneg"] = 100-dn["prepos"]
				dn["categories"] = []
				dn["has"] = False
				if request.user:
					if request.user.data > "":
						myfilms = request.user.data.split(' ')
						for j in range(0, len(myfilms)):
							if i.id == (int)(myfilms[j]):
								dn["has"] = True;
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
				dn["cost"] = i.cost
				dn["prepos"] = (i.pos*100/(i.pos+i.neg))
				dn["preneg"] = 100-dn["prepos"]
				dn["categories"] = []
				dn["has"] = False
				if request.user:
					if request.user.data > "":
						myfilms = request.user.data.split(' ')
						for j in range(0, len(myfilms)):
							if i.id == (int)(myfilms[j]):
								dn["has"] = True;
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
def getfilm(request, film):
	has = False
	i = Film.objects.get(id=film)
	if not request.user.is_anonymous:
		if request.user.data > "":
			myfilms = request.user.data.split(' ')
			for j in range(0, len(myfilms)):
				if i.id == (int)(myfilms[j]):
					has = True;
		if (has or i.cost == 0) and request.user.get_age() >= i.age:
			dn = {}
			dn["id"] = i.id
			dn["name"] = i.name
			dn["year"] = i.year
			dn["date"] = i.date
			dn["country"] = i.country
			dn["image"] = i.image.url
			dn["pos"] = i.pos
			dn["neg"] = i.neg 
			dn["director"] = i.director
			dn["roles"] = i.roles
			dn["prepos"] = (i.pos*100/(i.pos+i.neg))
			dn["preneg"] = 100-dn["prepos"]
			dn["categories"] = []
			dn["link"] = i.link
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
			return render(request, 'movie/film.html', {"f":dn})
	return redirect('/')












# def SetListBlockchain(blocklist):
#     db = json.load(open('movie/database.json', encoding='utf8'))
#     hdict={"Номер СНИЛСа:" : blocklist[i].data[0], "Статус утверждения возраста:" : blocklist[i].data[1], "hash" : blocklist[i].hash}
#     db['Data'].append(hdict)

#     with open('movie/database.json', mode='r', encoding='utf-8') as feedsjson:
# 		d = json.load(feedsjson)
# 	d["Data"][len(d["Data"])] = 
#     with open('movie/database.json', 'w', encoding='utf-8') as output:
#         output.write(json.dumps(db, ensure_ascii=False, indent=4))
#         output.close()
#def create_genesis_block():#Генерация начального блока
    #return Block(0, date.datetime.now(), "Genesis Block", "0")

# def next_block(index,hash, data):
#     this_index = index + 1
#     this_timestamp = date.datetime.now()

#     this_data = data

#     this_hash = hash

#     return Block(this_index, this_timestamp, this_data, this_hash)

def addBlockCH(snils):
    data = [snils, "Moderation...", "123"]
    db = json.load(open('movie/database.json', encoding='utf8'))
  #   with open('movie/database.json', mode='r', encoding='utf-8') as feedsjson:
		# db = json.load(feedsjson)
    #previous_block = next_block(len(db["Data"])-1,db["Data"][len(db["Data"])-1]["hash"], data)
    hdict={"Номер СНИЛСа:" : snils, "Статус утверждения возраста:" : "Moderation...", "hash" : "0"}
    db["Data"].append(hdict)
  #   with open('movie/database.json', mode='w', encoding='utf-8') as feedsjson:
		# json.dump(db, feedsjson)
    with open('movie/database.json', 'w', encoding='utf-8') as output:
        output.write(json.dumps(db, ensure_ascii=False, indent=4))
        output.close()



 

''' 

''' 
# def new user 

# open a json file as js 
# hash = js[len(js)-1]['hash'] 
# snils = request.post.get('snils') 
# status = request.post.get('status utv') 

# dict = {'snils':snils, 'status':status, 'hash':hash} 
# js.append(dict) 
# with open... 