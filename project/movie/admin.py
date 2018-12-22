from django.contrib import admin
from .models import *

from django.contrib.auth import get_user_model
from .forms import UserAdminCreationForm, UserAdminChangeForm
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.http import Http404
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
User = get_user_model()

class UserAdmin(BaseUserAdmin):
	form = UserAdminChangeForm
	add_form = UserAdminCreationForm

	list_display = ('login', 'active')
	list_filter = ('admin',)
	fieldsets = (
		(None, {'fields': ('login', 'password')}),
		('Personal info', {'fields': ('date','data')}),
		('Properties', {'fields': ('admin',)}),
	)
	add_fieldsets = (
		(None, {
			'classes':('wide',),
			'fields': ('login', 'password1', 'password2')}
		),
	)
	search_fields = ('login',)
	ordering = ('login',)
	filter_horizontal = ()

class FilmAdmin:
	list_display = ('id', 'name')
# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Film)