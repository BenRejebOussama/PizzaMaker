from rest_framework import serializers

from api.models import Pizza, Ingredients


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ['id', 'name']


class PizzaSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField()

    class Meta:
        model = Pizza
        fields = ['name', 'price', 'ingredients']

    def get_ingredients(self, obj):
        return obj.ingredients.values_list('name', flat=True)