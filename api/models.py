from django.db import models


class Ingredients(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Pizza(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=4)
    ingredients = models.ManyToManyField(Ingredients)

    def __str__(self):
        return self.name
