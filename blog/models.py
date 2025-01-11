from django.db import models



class Post(models.Model):
    restuarant_id = models.CharField(max_lenth=250)
    created_date = models.CharField(max_lenth=250)
    post_content = models.CharField(max_lenth=250)
    visit_date = models.CharField(max_lenth=250)
    rate_1 = models.CharField(max_lenth=250)
    rate_2 = models.CharField(max_lenth=250)
    rate_3 = models.CharField(max_lenth=250)
    rate_4 = models.CharField(max_lenth=250)

    class Meta:
        ordering = ('created_date')

    def __str__(self):
        return f'Data wizyty: {self.visit_date} Post: {self.post_content[100:]}...'

class Restaurant(models.Model):
    city_id = models.CharField(max_lenth=250)
    name = models.CharField(max_lenth=250)
    description = models.CharField(max_lenth=250)
    colorsys = models.CharField(max_lenth=250)

    class Meta:
        ordering = ('created_date')

    def __str__(self):
        return f'Data wizyty: {self.visit_date} Post: {self.post_content[100:]}...'

class City(models.Model):
    city_id = models.CharField(max_lenth=250)
    country_id = models.CharField(max_lenth=250)
    name = models.CharField(max_lenth=250)

    class Meta:
        ordering = ('created_date')

    def __str__(self):
        return f'Data wizyty: {self.visit_date} Post: {self.post_content[100:]}...'


class Conutry(models.Model):
    name = models.CharField(max_lenth=250)

    class Meta:
        ordering = ('created_date')

    def __str__(self):
        return f'Data wizyty: {self.visit_date} Post: {self.post_content[100:]}...'


class Image(models.Model):
    date = models.CharField(max_lenth=250)
    restaurant_id = models.CharField(max_lenth=250)
    recipe_id = models.CharField(max_lenth=250)

    class Meta:
        ordering = ('created_date')

    def __str__(self):
        return f'Data wizyty: {self.visit_date} Post: {self.post_content[100:]}...'


class Recipe(models.Model):
    date = models.CharField(max_lenth=250)
    image = models.CharField(max_lenth=250)
    name = models.CharField(max_lenth=250)
    description = models.CharField(max_lenth=250)

    class Meta:
        ordering = ('created_date')

    def __str__(self):
        return f'Data wizyty: {self.visit_date} Post: {self.post_content[100:]}...'