import base64
import os
from datetime import datetime

from django.contrib.contenttypes.models import ContentType
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from PIL import Image as PILImage
from .models import City, Restaurant, Post, Country, Image
from .forms import PostForm
from django.http import JsonResponse
import logging
import json
from io import BytesIO


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
        post_text = request.POST.get('post_text')
        price_rating = request.POST.get('price_rating')
        restaurant_rating = request.POST.get('restaurant_rating')
        overall_rating = request.POST.get('overall_rating')
        taste_rating = request.POST.get('taste_rating')
        restaurant_description = request.POST.get('restaurant_description')

        # # Pobranie obiektu kraju
        country = get_object_or_404(Country, id=country_id)
        # # Pobranie obiektu miasta (jeśli wybrane)
        city = City.objects.get(id=city_id) if city_id else None
        # TODO Dodać wyszukanie jeżeli podana nazwa restauracji znajduje sie już w bazie
        restaurant = Restaurant.objects.create(
                city = city,
                name = restaurant_name,
                description = restaurant_description,
                    )



       # Utworzenie nowego postu
        post = Post.objects.create(
            title=post_title,
        body = post_text,
        created = datetime.now(),
        restaurant = restaurant,
        visit_date = visit_date,
        taste_rating = taste_rating,
        price_rating = price_rating,
        restaurant_rating =restaurant_rating,
        overall_rating =overall_rating
        )
        post_id = post.id
        # Przekierowanie lub renderowanie po zapisaniu

        return redirect(f'/upload_photo/{post_id}/')  # Zmień to na odpowiednią stronę
        #return redirect('blog:upload_photo')

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
        data = json.loads(request.body)
        country_name = data.get("name", "").strip()
        if country_name:
            # Tworzenie nowego kraju
            new_country = Country.objects.create(name=country_name)
            return JsonResponse({"success": True, "country_id": new_country.id, "country_name": new_country.name})
        else:
            return JsonResponse({"success": False, "error": "Nazwa kraju nie może być pusta."}, status=400)
    return JsonResponse({"success": False, "error": "Nieprawidłowa metoda."}, status=405)



def load_add_country_modal(request):
    return render(request, "blog/modal/add_country_modal.html")

def add_city(request):
    if request.method == "POST":
        data = json.loads(request.body)
        city_name = data.get("cityName", "").strip()
        country_id = data.get("countryId", "").strip()
        if city_name:
            # Tworzenie nowego miasta
            new_city = City.objects.create(name=city_name, country_id=country_id)


            return JsonResponse({"success": True, "city_id": new_city.id, "city_name": new_city.name})
        else:
            return JsonResponse({"success": False, "error": "Nazwa miasta nie może być pusta."}, status=400)
    return JsonResponse({"success": False, "error": "Nieprawidłowa metoda."}, status=405)

def load_add_city_modal(request):
    return render(request, "blog/modal/add_city_modal.html")



def upload_photo(request, post_id):
    post = get_object_or_404(Post, id=post_id)


    if request.method == 'POST':

        if 'formFileMultiple' not in request.FILES:
            return JsonResponse({'error': 'Nie przesłano pliku!'}, status=400)

        images = request.FILES.getlist('formFileMultiple')  # Obsługa wielu plików

        for image in images:
            relative_path = f'{datetime.now().strftime('%Y/%m/%d')}/ {image.name}'
            full_path = os.path.join(settings.MEDIA_ROOT,relative_path)

            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            default_storage.save(full_path, ContentFile(image.read())) # Zapis pliku

            #TODO Dodawanie obiektu image i wiazanie go z konkretnym postem

            # Utworzenie nowego postu
            new_image = Image.objects.create(
                image=relative_path,
            add_date = datetime.now(),
            title ="",
                post = post,
            object_id = post.id,
            content_type = ContentType.objects.get_for_model(Post)

            )

        return redirect('blog:accept_new_post')  # Zmień to na odpowiednią stronę


    return render(request, 'blog/post/upload_photo.html', {'post': post})


def post_detail(request, post_id):
    # Pobierz post o danym id, jeśli nie istnieje, zwróć 404
    post = get_object_or_404(Post, pk=post_id)
    images = Image.objects.filter(post=post)  # Pobieranie zdjęć powiązanych z postem


    resized_images = []

    for image in images:
        img = PILImage.open(image.image)
        img = img.convert('RGB')

        # base_width = 800
        # w_percent = (base_width / float(img.size[0]))
        # h_size = int((float(img.size[1]) * float(w_percent)))
        # img = img.resize((base_width, h_size), PILImage.Resampling.LANCZOS)

        base_width = 600
        base_height = 400  # Nowa, wymuszona wysokość

        img = img.resize((base_width, base_height), PILImage.Resampling.LANCZOS)

        temp_file = BytesIO()
        img.save(temp_file, format='JPEG')
        temp_file.seek(0)

        # Kodowanie do base64
        base64_image = base64.b64encode(temp_file.read()).decode('utf-8')
        resized_images.append(
            {
                'base64': base64_image,
                'title': image.title,
                'date': image.add_date,

            }
        )

    taste_rating = post.taste_rating
    price_rating = post.price_rating
    restaurant_rating = post.restaurant_rating
    overall_rating = post.overall_rating



    taste_rating_full_stars = range(taste_rating)
    taste_rating_empty_stars = range(6-taste_rating)

    price_rating_full_stars = range(price_rating)
    price_rating_empty_stars = range(6-price_rating)

    restaurant_rating_full_stars = range(restaurant_rating)
    restaurant_rating_empty_stars = range(6-restaurant_rating)

    overall_rating_full_stars = range(overall_rating)
    overall_rating_empty_stars = range(6-overall_rating)



    # Przekaż post do szablonu
    return render(request, 'blog/post/post_detail.html', {
                                                        'post': post,
                                                        'images':resized_images,


                                                        'taste_rating_full_stars' :taste_rating_full_stars,
                                                        'taste_rating_empty_stars' : taste_rating_empty_stars,

                                                        'price_rating_full_stars' :price_rating_full_stars,
                                                        'price_rating_empty_stars' : price_rating_empty_stars,

                                                        'restaurant_rating_full_stars' :restaurant_rating_full_stars,
                                                        'restaurant_rating_empty_stars' : restaurant_rating_empty_stars,

                                                        'overall_rating_full_stars' : overall_rating_full_stars,
                                                        'overall_rating_empty_stars' :overall_rating_empty_stars
                                                                                }
                  )
