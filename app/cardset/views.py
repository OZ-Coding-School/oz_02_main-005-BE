from django.shortcuts import render
from concurrent.futures import ThreadPoolExecutor
from .models import CardSet
import pandas as pd
import datetime
# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CardSetSerializer
from card.models import Card
executor = ThreadPoolExecutor(max_workers=5)

class CardSetView(APIView):
    def post(self, request):
        serializer = CardSetSerializer(
            cardset_title=request.data.cardset_title,
            cardset_public=request.data.cardset_public,
            created_at = datetime.now())


        csv=pd.read_csv(request.FILES('file'))

        for _, row in csv.iterrows():
            Card.objects.create(
                card_question=csv.iloc[row]['card_question'],
                card_answer=csv.iloc[row]['card_answer'],
                created_at=datetime.now()

            )
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
        

    def get(self,request):
        cardset_data =CardSet.objects.all()
        serializer = CardSetSerializer(cardset_data,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def getSave(self,request):
        cardset_save_data = CardSet.objects.filter(cardset_down=1,many=True)
        serializer = CardSetSerializer(cardset_save_data,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def update(self,request,cardset_id):
        cardset_update= CardSet.objects.filter(id=cardset_id)
        cardset_update.update(cardset_title=request.data.cardset_title,modified_at = datetime.now())

        serializer= CardSetSerializer(cardset_update,many=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
            