from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Comment
from .serializers import CommentSerializer,CommentGetSerializer
from drf_yasg.utils import swagger_auto_schema

from cardset.models import CardSet
from drf_yasg import openapi
class CreateComment(APIView):
    #permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_QUERY, description="Name of the item", type=openapi.TYPE_STRING)
        ]
    )
    def post(self, request, cardset_id):

        try:
            cardset = CardSet.objects.get(pk=cardset_id)
        except CardSet.DoesNotExist:
            return Response({"error": "Cardset not found"}, status=status.HTTP_404_NOT_FOUND)
        
        data_with_comment_id = request.data.copy()
        data_with_comment_id['cardset'] = cardset.id
        serializer = CommentSerializer(data=data_with_comment_id)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# 대댓글 생성하기_동기
class CreateRecomment(APIView):
    #permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(request_body=CommentSerializer)
    def post(self, request, cardset_id, parent_id):

        try:
            cardset = CardSet.objects.get(pk=cardset_id)
        except CardSet.DoesNotExist:
            return Response({"error": "Cardset not found"}, status=status.HTTP_404_NOT_FOUND)
        
        data_with_recomment_id = request.data.copy()
        data_with_recomment_id['cardset'] = cardset.id
        data_with_recomment_id['parent'] = parent_id
        serializer = CommentSerializer(data=data_with_recomment_id)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# 댓글, 대댓글 리스트 조회_동기
class CommentList(APIView):
    #permission_classes = [IsAuthenticated]

    def get(self, request, cardset_id):
        try:
            cardset = CardSet.objects.get(pk=cardset_id)
        except cardset.DoesNotExist:
            return Response({"error": "Cardset not found"}, status=status.HTTP_404_NOT_FOUND)
        
        comments = Comment.objects.filter(parent=None, cardset=cardset)
        
        serializer = CommentGetSerializer(comments, many=True)
        return Response(serializer.data)
    
# 댓글, 대댓글 수정하기_동기    
class UpdateComment(APIView):
    #permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=CommentSerializer)
    def post(self, request, comment_id): #*args, **kwargs
        data = request.data
        new_content = data.get("content")

        if not new_content:
            return Response(
                {"error": "new_content are required"}, status=400
            )

        try:
            comment = Comment.objects.get(id=comment_id)
            comment.content = new_content
            comment.save()
            serializer = CommentSerializer(comment)
            return Response(serializer.data, status=200)
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
# 댓글, 대댓글 삭제하기_동기        
class DeleteComment(APIView):
    #permission_classes = [IsAuthenticated]

    def post(self, request, comment_id): #*args, **kwargs

        try:
            comment = Comment.objects.get(id=comment_id)
            comment.delete()
            return Response({"message": "Comment deleted successfully"}, status=200)
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
