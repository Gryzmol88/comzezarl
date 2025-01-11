from django.shortcuts import render

# Create your views here.
def index_page(request):
    return render(request, 'blog/post/index.html')

def news_page(request):
    return render(request, 'blog/post/news.html')
def byd_page(request):
    return render(request, 'blog/post/byd.html')
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

