from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import F
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from .serializers import FolderSerializer, FolderGetSerializer
from .models import Folder
# from rest_framework.permissions import IsAuthenticated

# Create your views here.
# Folder 생성_동기
class CreateFolder(APIView):
    #permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=FolderSerializer)
    def post(slef, request): 
        serializer = FolderSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400) 
    
class UpdateFolder(APIView):
    #permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=FolderSerializer)
    def post(self, request, folder_id): 
        data = request.data
        new_title = data.get("folder_title")

        if not new_title:
            return Response(
                {"error": "folder_title are required"}, status=400
            )

        try:
            folder = Folder.objects.get(id=folder_id)
            folder.folder_title = new_title
            folder.save()
            serializer = FolderSerializer(folder)
            return Response(serializer.data, status=200)
        except Folder.DoesNotExist:
            return Response({"error": "Folder not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
class DeleteFolder(APIView):
    #permission_classes = [IsAuthenticated]

    def post(self, request, folder_id): 
        data = request.data

        try:
            folder = Folder.objects.get(id=folder_id)
            folder.delete()
            return Response({"message": "Folder deleted successfully"}, status=200)
        except Folder.DoesNotExist:
            return Response({"error": "Folder not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
#<최신순으로 조회하는 기능>_동기
class FolderList(APIView):
    #permission_classes = [IsAuthenticated]

    def get(self, request, member_id, *args, **kwargs):
       if member_id:
            folders = Folder.objects.all.filter(member_id=member_id).order_by(F('modified_at').desc())
       else:
            folders = Folder.objects.none()
       serializer = FolderGetSerializer(folders, many=True)
       return Response(serializer.data, status=status.HTTP_200_OK)
        


