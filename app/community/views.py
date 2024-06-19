from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import RateSerializer, RateCreateSerializer, CopyCardsetRequestSerializer
from django.db.models import Avg, Q
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from .models import Mileage
from card.models import Card
from cardset.models import CardSet
from folders.models import Folder
from cardset.serializers import CardSetSerializer
from drf_yasg import openapi
# Create your views here.
from drf_yasg.utils import swagger_auto_schema
# 인기순
class RateListView(generics.ListAPIView):
    serializer_class = CardSetSerializer
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_QUERY, description="Name of the item", type=openapi.TYPE_STRING)
        ]
    )
    

    def get_queryset(self):
        return CardSet.objects.filter(cardset_public=True, cardset_down=True).annotate(avg_rate=Avg('rate__rate')).order_by('-avg_rate', 'created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        response_data = []
        for card_set_data in serializer.data:
            card_set = queryset.get(pk=card_set_data['cardset_id'])
            avg_rate = card_set.rate_set.aggregate(average=Avg('rate'))['average']
            cards = Card.objects.filter(cardset=card_set)
            cards_count = cards.count()

            card_set_data.update({
                'avg_rate': avg_rate,
                'cards_count': cards_count,
            })
            response_data.append(card_set_data)

        return Response(response_data)


# 최신순
class NewListView(generics.ListAPIView):
    serializer_class = CardSetSerializer

    def get_queryset(self):
        return CardSet.objects.filter(cardset_public=True, cardset_down=True).order_by('-created_at')
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        response_data = []
        for card_set_data in serializer.data:
            card_set = queryset.get(pk=card_set_data['cardset_id'])
            avg_rate = card_set.rate_set.aggregate(average=Avg('rate'))['average']
            cards = Card.objects.filter(cardset=card_set)
            cards_count = cards.count()

            card_set_data.update({
                'avg_rate': avg_rate,
                'cards_count': cards_count,
            })
            response_data.append(card_set_data)

        return Response(response_data)

# 저장순
class SaveListView(generics.ListAPIView):
    serializer_class = CardSetSerializer

    def get_queryset(self):
        return CardSet.objects.filter(cardset_public=True, cardset_down=True).order_by('-down_count')
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        response_data = []
        for card_set_data in serializer.data:
            card_set = queryset.get(pk=card_set_data['cardset_id'])
            avg_rate = card_set.rate_set.aggregate(average=Avg('rate'))['average']
            cards = Card.objects.filter(cardset=card_set)
            cards_count = cards.count()

            card_set_data.update({
                'avg_rate': avg_rate,
                'cards_count': cards_count,
            })
            response_data.append(card_set_data)

        return Response(response_data)

# 별점
@extend_schema(
    request=RateCreateSerializer,
    responses={201: RateSerializer, 400: 'Bad Request', 404: 'Not Found'}
)

@api_view(['POST'])
def cardset_rate(request, pk):
    try:
        card_set = CardSet.objects.get(pk=pk, cardset_public=True, cardset_down=True)
    except CardSet.DoesNotExist:
        return Response({'detail': 'Cardset not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = RateCreateSerializer(data=request.data)
    if serializer.is_valid():
        rate = serializer.save(cardset=card_set)

        # 사용자에게 마일리지 적립
        if request.user.is_authenticated:
            user_mileage, created = Mileage.objects.get_or_create(member=request.user)
            user_mileage.mileage_amount += 5
            user_mileage.save()
        else:
            # 인증되지 않은 사용자에게 별도의 처리가 필요한 경우
            pass

        return Response(RateSerializer(rate).data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 검색
@extend_schema(
    parameters=[
        OpenApiParameter(name='q', description='Search query', required=False, type=str)
    ],
    responses={200: CardSetSerializer(many=True)}
)
@api_view(['GET'])
def cardset_search(request):
    query = request.GET.get('q')
    if query:
        cardsets = CardSet.objects.filter(
            Q(cardset_title__icontains=query) | Q(member__display_name__icontains=query)
        )
    else:
        cardsets = CardSet.objects.all()
    return Response(CardSetSerializer(cardsets, many=True).data)


# 저장
@extend_schema(
    request=CopyCardsetRequestSerializer,
    responses={201: 'Cardset copied successfully', 400: 'Bad Request', 404: 'Not Found'}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cardset_save(request):
    try:
        with transaction.atomic():
            cardset_id = request.data.get('cardset_id')
            
            original_cardset = CardSet.objects.get(pk=cardset_id)
            original_cards = Card.objects.filter(cardset=original_cardset)
            
            save_folder, created = Folder.objects.get_or_create(
                member=request.user,
                folder_title='save',
                defaults={'folder_title': 'save'}
            )
            
            new_cardset = CardSet.objects.create(
                folder=save_folder,
                cardset_title=original_cardset.cardset_title,
                cardset_public=False,
                cardset_down=False,
                member=request.user,
                down_count=0
            )
            
            for card in original_cards:
                Card.objects.create(
                    cardset=new_cardset,
                    card_question=card.card_question,
                    card_answer=card.card_answer,
                    question_type=card.question_type,
                    question_option=card.question_option
                )

            original_cardset.down_count += 1
            original_cardset.save()
            
            user_mileage, created = Mileage.objects.get_or_create(member=request.user, defaults={'mileage_amount': 0})
            if user_mileage.mileage_amount >= 10:
                user_mileage.mileage_amount -= 10
                user_mileage.save()
            else:
                return Response({"error": "Insufficient mileage"}, status=status.HTTP_400_BAD_REQUEST)

            original_cardset_mileage, created = Mileage.objects.get_or_create(member=original_cardset.member, defaults={'mileage_amount': 0})
            original_cardset_mileage.mileage_amount += 10
            original_cardset_mileage.save()
            
            return Response({"message": "Cardset copied successfully"}, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
