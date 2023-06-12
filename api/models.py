from django.db import models


class Ingredients(models.Model):
    name = models.CharField(max_length=200)


