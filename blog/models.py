from django.conf import settings
from django.db import models
from django.db.models import TextField, ForeignKey
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# TODO //TODO Warning M:\Michal\Programowanie\pythonProject\comZezarl\venv\Lib\site-packages\django\db\models\fields\__init__.py:1665: RuntimeWarning: DateTimeField Post.visit_date received a naive datetime (2025-03-12 00:00:00) while time zone support is active.
#   warnings.warn(

class Country(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, blank=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='cities')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, blank=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return f'Kraj: {self.country.name} Miasto: {self.name}'


class Restaurant(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='restaurants')
    name = models.CharField(max_length=100)
    description = models.TextField()
    # TODO: Usunać color z restauracji???
    color = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, blank=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return f'Restauracja: {self.name}'




class Recipe(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=250)
    description = models.TextField()
    slug = models.SlugField(max_length=200, blank=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return f'Tytuł przepisu: {self.title}'


class Post(models.Model):
    RATE = [
        (1, "Bardzo słabo"),
        (2, "Słabo"),
        (3, "Średnio"),
        (4, "Dobrze"),
        (5, "Bardzo dobrze"),
        (6, "Celująco"),
    ]
    title = models.CharField(max_length=250)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE, related_name='posts')
    visit_date = models.DateTimeField()
    taste_rating = models.IntegerField(choices=RATE)
    price_rating = models.IntegerField(choices=RATE)
    restaurant_rating = models.IntegerField(choices=RATE)
    overall_rating = models.IntegerField(choices=RATE)
    slug = models.SlugField(max_length=200, blank=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        if len(self.body) > 100:
            return f'Data wizyty: {self.created} Post: {self.body[100:]}...'
        else:
            return f'Data wizyty: {self.created} Post: {self.body}'

    def get_taste_rating_display(self):
        return dict(self.RATE).get(self.taste_rating, "Brak oceny")

    def get_price_rating_display(self):
        return dict(self.RATE).get(self.price_rating, "Brak oceny")

    def get_restaurant_rating_display(self):
        return dict(self.RATE).get(self.restaurant_rating, "Brak oceny")

    def get_overall_rating_display(self):
        return dict(self.RATE).get(self.overall_rating, "Brak oceny")

class Image(models.Model):
    image =models.ImageField()
    add_date = models.DateField()
    title = models.CharField(max_length=100)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    #GenericForeignKey
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # Model docelowy
    object_id = models.PositiveIntegerField()  # ID obiektu docelowego
    content_object = GenericForeignKey('content_type', 'object_id')  # Łączy content_type i object_id
    slug = models.SlugField(max_length=200, blank=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return f'Tytul: {self.title}'
