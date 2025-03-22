from django.contrib import admin
from .models import Post, Country, Recipe, Image, Restaurant, City




class PostAdmin(admin.ModelAdmin):
    list_display = (
    'id','title', 'created')  # Kolumny w widoku listy
    list_filter = ('taste_rating', 'price_rating', 'restaurant_rating', 'overall_rating')  # Filtry po kategoriach
    search_fields = ('title',)  # Wyszukiwanie po tytule

    # Definiowanie formy edycji (np. domyślne wartości)
    fieldsets = (
        (None, {
            'fields': (
            'title', 'body', 'taste_rating', 'price_rating', 'restaurant_rating', 'overall_rating', 'visit_date')
        }),
        ('Dodatkowe informacje', {
            'fields': ('slug',),
            'classes': ('collapse',),  # Ukryte pole
        }),
    )


# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Country)
admin.site.register(Recipe)
admin.site.register(Image)
admin.site.register(Restaurant)
admin.site.register(City)
