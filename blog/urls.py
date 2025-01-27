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
    path('newpost/',views.add_new_post, name='add_new_post'),
    path('newpost/<int:country_id>/cities/', views.cities_by_country, name='cities_by_country'),
    path('accept_new_post/',views.accept_new_post, name='accept_new_post'),
    path("load_add_country_modal/", views.load_add_country_modal, name="load_add_country_modal"),
    path("add_country/", views.add_country, name="add_country"),

]