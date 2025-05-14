from xml.etree.ElementInclude import include

from django.urls import path
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static

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
    path("load_add_city_modal/", views.load_add_city_modal, name="load_add_city_modal"),
    path("add_city/", views.add_city, name="add_city"),
    path("upload_photo/<int:post_id>/",views.upload_photo, name="upload_photo"),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)