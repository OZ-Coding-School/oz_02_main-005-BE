from rest_framework import serializers
from .models import Folder


class FolderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Folder
        fields = "__all__"

class FolderGetSerializer(serializers.ModelSerializer):
    display_name = serializers.ReadOnlyField(source="member.display_name")

    class Meta:
        model = Folder
        fields = ['id', 'folder_title', 'display_name', 'created_at','modified_at']