from rest_framework import serializers
from .models import CardSet

class CardSetSerializer(serializers.Serializer):
    class Meta:
        model=CardSet
        fields= ['id','cardset_title','cardset_public','created_at','modified_at']