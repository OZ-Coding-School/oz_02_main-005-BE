from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from .models import Member
from .serializers import MemberSerializer, LoginSerializer, TokenResponseSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.settings import api_settings

class MemberCreate(generics.CreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': {
                'id': user.member_id,
                'account': user.account,
                'email': user.member_email,
                'nickname': user.display_name,
            },
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }, status=status.HTTP_201_CREATED)

class MemberLogin(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=LoginSerializer,
        responses={
            200: TokenResponseSerializer,
            401: OpenApiResponse(description='Invalid Credentials'),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account = serializer.validated_data['account']
        password = serializer.validated_data['password']

        user = authenticate(request, username=account, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(
            {'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED
        )

class MemberLogout(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: OpenApiResponse(description='Logout successful'),
            401: OpenApiResponse(description='Invalid token'),
        },
    )
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh')
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=status.HTTP_200_OK)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'account'

    def validate(self, attrs):
        account = attrs.get(self.username_field)
        password = attrs.get("password")

        try:
            user = Member.objects.get(account=account)
        except Member.DoesNotExist:
            raise AuthenticationFailed('No active account found with the given credentials')

        if not user.check_password(password):
            raise AuthenticationFailed('No active account found with the given credentials')

        refresh = self.get_token(user)

        data = {}
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, user)

        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return HttpResponse("Welcome to the Home Page")