from rest_framework import serializers
from .models import Member

class MemberSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Member
        fields = [
            "member_id",
            "account",
            "member_email",
            "display_name",
            "created_at",
            "modified_at",
            "daily_accom",
            "password",
        ]

    def create(self, validated_data):
        user = Member(
            account=validated_data["account"],
            member_email=validated_data["member_email"],
            display_name=validated_data["display_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    account = serializers.CharField()
    password = serializers.CharField(write_only=True)

class TokenResponseSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
