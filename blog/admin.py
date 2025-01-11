from django.contrib import admin
from .models import Post, Country, Recipe, Image, Restaurant, City


# Register your models here.
admin.site.register(Post)
admin.site.register(Country)
admin.site.register(Recipe)
admin.site.register(Image)
admin.site.register(Restaurant)
admin.site.register(City)

