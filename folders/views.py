from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import F

from .serializers import FolderSerializer, FolderGetSerializer
from .models import Folder
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
import asyncio
from asgiref.sync import sync_to_async, async_to_sync
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Folder 생성_동기
class CreateFolder(APIView):
    #permission_classes = [IsAuthenticated]

    def post(slef, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = FolderSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)