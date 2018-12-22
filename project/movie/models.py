from django.db import models

# Create your models here.

class Film(models.Model):
	name = models.CharField(max_length=255)
	year = models.IntegerField(default=0)
	date = models.CharField(max_length=100, verbose_name="date of release")
	age = models.IntegerField()
	country = models.CharField(max_length=100)
	time = models.IntegerField()
	director = models.CharField(max_length=100)
	pos = models.IntegerField()
	neg = models.IntegerField()
	image = models.FileField()
	categories = models.CharField(max_length=255, default="others")
	small_title = models.TextField()
	large_title = models.TextField()
	trailer = models.CharField(max_length=100)

	def __str__(self):
		return name
