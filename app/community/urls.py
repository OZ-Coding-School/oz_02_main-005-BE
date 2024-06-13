from django.urls import path
from .views import (
    CardsetListView, RateListView, NewListView, SaveListView, CardsetDetailView,
    rate_cardset, search_cardset, save_cardset
)

urlpatterns = [
    path('cardsets/', CardsetListView.as_view(), name='cardset-list'),
    path('cardsets/rate/', RateListView.as_view(), name='rate-list'),
    path('cardsets/new/', NewListView.as_view(), name='new-list'),
    path('cardsets/save/', SaveListView.as_view(), name='save-list'),
    path('cardsets/<int:pk>/', CardsetDetailView.as_view(), name='posting'),
    path('cardsets/<int:pk>/rate/', rate_cardset, name='rate-cardset'),
    path('cardsets/search/', search_cardset, name='search-cardset'),
    path('cardsets/save_cardset/', save_cardset, name='save_cardset'),
]
