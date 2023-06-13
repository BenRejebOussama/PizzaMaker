from rest_framework import serializers

from api.models import Pizza, Ingredients


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ['id','name']


class PizzaSerializer(serializers.ModelSerializer):
    ingredients = IngredientsSerializer(read_only=True, many=True)

    class Meta:
        model = Pizza
        fields = ['name', 'price', 'ingredients']
