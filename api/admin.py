from django.contrib import admin

from api.models import Pizza, Ingredients


@admin.register(Ingredients)
class GenericAdmin(admin.ModelAdmin):
    pass


@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
