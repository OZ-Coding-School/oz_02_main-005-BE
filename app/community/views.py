from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Cardset, Card, Folder, Member
from .serializers import CardsetSerializer, CardSerializer, RateSerializer, RateCreateSerializer
from django.db.models import Avg, Q
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.db import transaction
from rest_framework.permissions import IsAuthenticated

# Create your views here.

# 작성순
class CardsetListView(generics.ListAPIView):
    serializer_class = CardsetSerializer

    def get_queryset(self):
        return Cardset.objects.filter(cardset_public=True, cardset_down=True)

# 인기순
class RateListView(generics.ListAPIView):
    serializer_class = CardsetSerializer

    def get_queryset(self):
        return Cardset.objects.filter(cardset_public=True, cardset_down=True).annotate(avg_rate=Avg('rate__rate')).order_by('-avg_rate', 'created_at')

# 최신순
class NewListView(generics.ListAPIView):
    serializer_class = CardsetSerializer

    def get_queryset(self):
        return Cardset.objects.filter(cardset_public=True, cardset_down=True).order_by('-created_at')

# 저장순
class SaveListView(generics.ListAPIView):
    serializer_class = CardsetSerializer

    def get_queryset(self):
        return Cardset.objects.filter(cardset_public=True, cardset_down=True).order_by('-down_count')

# 카드뭉치 정보
class CardsetDetailView(generics.RetrieveAPIView):
    queryset = Cardset.objects.filter(cardset_public=True, cardset_down=True)
    serializer_class = CardsetSerializer

    def get(self, request, *args, **kwargs):
        card_set = self.get_object()
        avg_rate = card_set.rate_set.aggregate(average=Avg('rate'))['average']
        cards = Card.objects.filter(cardset=card_set)
        cards_count = cards.count()
        response_data = self.get_serializer(card_set).data
        response_data.update({
            'avg_rate': avg_rate,
            'cards_count': cards_count,
            'cards': CardSerializer(cards, many=True).data
        })
        return Response(response_data)

# 별점
@extend_schema(
    request=RateCreateSerializer,
    responses={201: RateSerializer, 400: 'Bad Request', 404: 'Not Found'}
)

@api_view(['POST'])
def cardset_rate(request, pk):
    try:
        card_set = Cardset.objects.get(pk=pk, cardset_public=True, cardset_down=True)
    except Cardset.DoesNotExist:
        return Response({'detail': 'Cardset not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = RateCreateSerializer(data=request.data)
    if serializer.is_valid():
        rate = serializer.save(cardset=card_set)
        return Response(RateSerializer(rate).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 검색
@extend_schema(
    parameters=[
        OpenApiParameter(name='q', description='Search query', required=False, type=str)
    ],
    responses={200: CardsetSerializer(many=True)}
)
@api_view(['GET'])
def search_cardset(request):
    query = request.GET.get('q')
    if query:
        cardsets = Cardset.objects.filter(
            Q(cardset_title__icontains=query) | Q(member__display_name__icontains=query)
        )
    else:
        cardsets = Cardset.objects.all()
    return Response(CardsetSerializer(cardsets, many=True).data)


# 저장
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cardset_save(request):

    try:
        with transaction.atomic():
            # 요청으로부터 cardset_id와 user_b_id를 가져옵니다.
            cardset_id = request.data.get('cardset_id')
            user_b_id = request.data.get('user_b_id')
            
            # 원본 cardset과 관련된 카드들을 가져옵니다.
            original_cardset = Cardset.objects.get(pk=cardset_id)
            original_cards = Card.objects.filter(cardset=original_cardset)
            
            # 대상 사용자를 가져옵니다.
            user_b = Member.objects.get(pk=user_b_id)
            
            # 대상 사용자가 이미 'save' 폴더를 가지고 있는지 확인하고, 없으면 생성합니다.
            save_folder, created = Folder.objects.get_or_create(
                member=user_b,
                folder_title='save',
                defaults={'folder_title': 'save'}
            )
            
            # 사용자 B를 위한 새로운 cardset을 생성합니다.
            new_cardset = Cardset.objects.create(
                folder=save_folder,
                cardset_title=original_cardset.cardset_title,
                cardset_public=False,
                cardset_down=False,
                member=user_b,
                down_count=0
            )
            
            # 원본 cardset의 각 카드를 새로운 cardset으로 복사합니다.
            for card in original_cards:
                Card.objects.create(
                    cardset=new_cardset,
                    card_question=card.card_question,
                    card_answer=card.card_answer,
                    question_type=card.question_type,
                    question_option=card.question_option
                )
            
            return Response({"message": "Cardset copied successfully"}, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
