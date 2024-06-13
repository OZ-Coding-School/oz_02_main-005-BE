from rest_framework import serializers
from .models import Folder, Cardset, Card, Rate

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'

class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = '__all__'
        # serializers.py

class RateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ['rate']


class CardsetSerializer(serializers.ModelSerializer):
    cards = CardSerializer(many=True, read_only=True)

    class Meta:
        model = Cardset
        fields = '__all__'

class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = '__all__'

class CopyCardsetRequestSerializer(serializers.Serializer):
    cardset_id = serializers.IntegerField()
    user_b_id = serializers.IntegerField()