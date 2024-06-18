from rest_framework import serializers
from .models import Rate

class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = '__all__'

class RateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ['rate']


class CopyCardsetRequestSerializer(serializers.Serializer):
    cardset_id = serializers.IntegerField()