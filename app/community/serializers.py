from rest_framework import serializers
from .models import Member, Folder, Cardset, Card, Rate

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['display_name']  # 필요한 필드를 지정

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'

class CardsetSerializer(serializers.ModelSerializer):
    cards = CardSerializer(many=True, read_only=True)
    member = MemberSerializer(read_only=True)

    class Meta:
        model = Cardset
        fields = '__all__'

class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = '__all__'

class RateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ['rate']

class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = '__all__'

class CopyCardsetRequestSerializer(serializers.Serializer):
    cardset_id = serializers.IntegerField()