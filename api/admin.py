from django.contrib import admin
from api.models import Pizza, Ingredients

@admin.register(Pizza, Ingredients)
class GenericAdmin(admin.ModelAdmin):
    pass