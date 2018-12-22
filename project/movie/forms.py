from django import forms
from .models import *

class FilmsForm(forms.ModelForm):

	class Meta:
		model = Films