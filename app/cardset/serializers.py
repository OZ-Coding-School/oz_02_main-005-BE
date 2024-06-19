from rest_framework import serializers
from .models import CardSet

class CardSetSerializer(serializers.ModelSerializer):
    class Meta:
        model=CardSet
        fields = '__all__'

