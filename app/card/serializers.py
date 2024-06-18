from rest_framework import serializers
from .models import Card
from cardset.serializers import CardSetSerializer

class CardSerializer(serializers.Serializer):
    query_set = CardSetSerializer(read_only=True)
    class Meta:
        model=Card
        fields = ['id','card_question','card_answer','question_type','quetion_option','created_at','modified_at','cardset']