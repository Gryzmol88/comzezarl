from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import request
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import City, Restaurant, Post, Country
from .forms import PostForm
from django.http import JsonResponse
import logging
import json



# Utwórz logger
logger = logging.getLogger(__name__)


# Create your views here.
def index_page(request):
    return render(request, 'blog/post/index.html')

def news_page(request):
    return render(request, 'blog/post/news.html')

def byd_page(request):

    restaurants = Restaurant.objects.filter(city__name='Bydgoszcz').select_related('city')


    return render(request, 'blog/post/byd.html', {'restaurants': restaurants})

def poland_page(request):
    return render(request, 'blog/post/poland.html')

def world_page(request):
    return render(request, 'blog/post/world.html')

def other_page(request):
    return render(request, 'blog/post/other.html')

def recipe_page(request):
    return render(request, 'blog/post/recipe.html')

def contact_page(request):
    return render(request, 'blog/post/contact.html')

# def add_new_post(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#     else:
#         form = PostForm()
#
#     context = {
#         'form':form,
#     }
#
#
#     return render(request, 'blog/post/new_post.html',context)



def add_new_post(request):
    if request.method == 'POST':

        # Odczytanie danych z formularza
        country_id = request.POST.get('country')
        city_id = request.POST.get('city')
        restaurant_name = request.POST.get('restaurant_name')
        post_title = request.POST.get('post_title')
        visit_date = request.POST.get('visit_date')
        # # Pobranie obiektu kraju
        country = get_object_or_404(Country, id=country_id)
        # # Pobranie obiektu miasta (jeśli wybrane)
        city = City.objects.get(id=city_id) if city_id else None

        # Logowanie ID kraju do konsoli

        # Utworzenie nowego postu
        # post = Post.objects.create(
        #     country=country,
        #     city=city,
        #     restaurant_name=restaurant_name,
        #     title=post_title,
        #     visit_date=visit_date
        # )

        # Przekierowanie lub renderowanie po zapisaniu

        return redirect('blog:accept_new_post')  # Zmień to na odpowiednią stronę

    # Jeśli nie POST, renderowanie formularza z listą krajów
    countries = Country.objects.all()
    return render(request, 'blog/post/new_post.html', {'countries': countries})

def cities_by_country(request, country_id):
    country = get_object_or_404(Country, id=country_id)
    cities = country.cities.all()
    cities_data = [{'id': city.id, 'name': city.name} for city in cities]

    return JsonResponse({'cities': cities_data})



def accept_new_post(request):
    return render(request, 'blog/post/accept_new_post.html')




def add_country(request):
    if request.method == "POST":
        try:
            # Odczytanie danych JSON z request.body
            data = json.loads(request.body)
            country_name = data.get("name", "").strip()

            if country_name:
                # Tworzenie nowego kraju
                new_country = Country.objects.create(name=country_name)
                return JsonResponse({
                    "success": True,
                    "country_id": new_country.id,
                    "country_name": new_country.name,
                })

            else:
                return JsonResponse({"success": False, "error": "Nazwa kraju nie może być pusta."}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Niepoprawny format JSON."}, status=400)
    return JsonResponse({"success": False, "error": "Nieprawidłowa metoda."}, status=405)



def load_add_country_modal(request):
    return render(request, "blog/modal/add_country_modal.html")


def add_city(request):
    if request.method == "POST":
        try:
            # Odczytanie danych JSON z request.body
            data = json.loads(request.body)
            city_name = data.get("name", "").strip()
            country_id = data.get("country_id")

            if city_name and country_id:
                # Pobranie kraju
                country = get_object_or_404(Country, id=country_id)

                # Tworzenie nowego miasta
                new_city = City.objects.create(name=city_name, country=country)
                return JsonResponse({
                    "success": True,
                    "city_id": new_city.id,
                    "city_name": new_city.name,
                })
            else:
                return JsonResponse({"success": False, "error": "Nazwa miasta i kraj są wymagane."}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Niepoprawny format JSON."}, status=400)
    return JsonResponse({"success": False, "error": "Nieprawidłowa metoda."}, status=405)


def load_add_city_modal(request):
    return render(request, "blog/modal/add_city_modal.html")
