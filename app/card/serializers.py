from rest_framework import serializers
from .models import Card
from cardset.serializers import CardSetSerializer

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model=Card
        fields = '__all__'