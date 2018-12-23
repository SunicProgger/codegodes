from django.db import models
from django.contrib.auth.models import (
	AbstractBaseUser, BaseUserManager
)
from datetime import datetime, date, time

# Create your models here.

class UserManage(BaseUserManager):
	def create_user(self, login, password=None, active=True, is_admin=False, is_superuser=False, date=None, data="", snils=""):
		if not login:
			raise ValueError("Users must have a login address")
		if not password:
			raise ValueError("Users must have a password")
		user_obj = self.model(login=login)
		user_obj.set_password(password)
		user_obj.active = active
		user_obj.admin = is_admin
		user_obj.is_superuser = is_superuser
		user_obj.date = date
		user_obj.data = data
		user_obj.snils = snils
		user_obj.save(using=self._db)
		return user_obj

	def create_superuser(self, login, password=None):
		user = self.create_user(login, password=password, is_admin=True)
		return user

class User(AbstractBaseUser):
	login        = models.CharField(max_length=255, unique=True)
	active       = models.BooleanField(default=True)
	admin        = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	date         = models.DateField(null=True, blank=True, verbose_name="date of birthday")
	data         = models.TextField(default="", null=True, blank=True, verbose_name="Activated movies")
	snils        = models.CharField(max_length=255, unique=True, default="snils", verbose_name="SNILS", null=True, blank=True)
	
	USERNAME_FIELD = 'login'
	REQUIRED_FIELDS = []

	objects = UserManage()

	def __str__(self):
		return self.login

	def get_age(self):
		a = (int)(datetime.today().strftime('%Y')) - (int)(self.date.strftime('%Y'))
		if (int)(self.date.strftime('%m')) > (int)(datetime.today().strftime('%m')):
			a -= 1
		if (int)(self.date.strftime('%m')) == (int)(datetime.today().strftime('%m')):
			if (int)(self.date.strftime('%d')) > (int)(datetime.today().strftime('%d')):
				a -= 1
		return a

	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_label):
		return True

	@property
	def is_active(self):
		return self.active
	def is_staff(self):
		return self.admin
	def is_admin(self):
		return self.admin
	def is_superuser(self):
		return self.admin

class Film(models.Model):
	name        = models.CharField(max_length=255)
	year        = models.IntegerField()
	date        = models.CharField(max_length=100, verbose_name="date of release", default="")
	age         = models.IntegerField()
	country     = models.CharField(max_length=100)
	cost        = models.IntegerField(default=0)
	time        = models.IntegerField(default=7200)
	director    = models.CharField(max_length=100)
	roles       = models.TextField(default="")
	pos         = models.IntegerField()
	neg         = models.IntegerField()
	image       = models.FileField()
	trailer     = models.CharField(max_length=100)
	link        = models.CharField(max_length=255, null=True, blank=True, default="")
	categories  = models.CharField(max_length=255, null=True, blank=True, default="")
	small_title = models.TextField()
	large_title = models.TextField()

	def __str__(self):
		return ((str)(self.id) + "." + self.name)
