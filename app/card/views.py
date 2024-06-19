from django.shortcuts import render
from rest_framework.views import APIView
from .models import Card
from rest_framework.response import Response
import datetime
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import CardSerializer
from rest_framework import status,permissions
# Create your views here.
class CardView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @swagger_auto_schema(request_body=CardSerializer)
    def post(self,request,cardset_id):
        serializer = CardSerializer(
            card_question = request.data.card_question,
            card_answer = request.data.card_answer,
            question_type = request.data.question_type,
            question_option = request.datat.quetion_option,
            created_at = datetime.now()
        )
        if serializer.is_valid():
            serializer.save(cardset=cardset_id)
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
class CardUpdateView(APIView):
    @swagger_auto_schema(request_body=CardSerializer)
    def post(self,request,cardset_id):
        card = Card.objects.get(cardset=cardset_id)
        card.objects.update(
            card_question = request.data.card_question,
            card_answer = request.data.card_answer,
            question_type = request.data.question_type,
            question_option = request.datat.quetion_option,
            modified_at = datetime.now())
        serializer=CardSerializer(data=card)
        serializer.save(raise_exception=True)
        return Response(serializer.data)
class CardGetView(APIView):
    def get(self,request,card_id):
        card = Card.objects.filter(id=card_id)
        serializer = CardSerializer(card)
        return Response(data=serializer.data,status=status.HTTP_200_OK)