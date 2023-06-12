from django.db import models


class Ingredients(models.Model):
    name = models.CharField(max_length=200)


class Pizza(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=2)
    ingredients = models.ManyToManyField(Ingredients)


