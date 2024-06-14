from rest_framework import serializers
from .models import Comment

class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

class CommentGetSerializer(serializers.ModelSerializer):
    display_name=serializers.ReadOnlyField(source='member.display_name')
    cardset_title=serializers.ReadOnlyField(source='cardset.cardset_title')
    reply = RecursiveSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content','display_name','cardset_title','created_at', 'modified_at','reply']

    def get_reply(self, instance):
    	# recursive
        serializer = self.__class__(instance.reply, many=True)
        serializer.bind('', self)
        return serializer.data