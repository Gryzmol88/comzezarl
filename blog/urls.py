from django.urls import path
from django.contrib import admin
from . import views

app_name = 'blog'

urlpatterns = [
    path('',views.news_page, name='news'),
    path('byd/',views.byd_page, name='byd'),
    path('poland/',views.poland_page, name='poland'),
    path('world/',views.world_page, name='world'),
    path('other/',views.other_page, name='other'),
    path('recipe/',views.recipe_page, name='recipe'),
    path('contact/',views.contact_page, name='contact'),
    path('newpost/',views.add_new_post, name='newpost'),
]