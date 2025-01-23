from django.shortcuts import render, get_object_or_404

from .models import City, Restaurant, Post, Country
from .forms import PostForm
from django.http import JsonResponse


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

def add_new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
    else:
        form = PostForm()

    context = {
        'form':form,
    }


    return render(request, 'blog/post/new_post.html',context)




def country_city_view(request):
    countries = Country.objects.all()
    return render(request, 'country_city_form.html', {'countries': countries})

def get_cities_by_country(request, country_id):
    cities = City.objects.filter(country_id=country_id).values('id', 'name')
    return JsonResponse(list(cities), safe=False)
