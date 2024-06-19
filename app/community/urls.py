from django.urls import path
from .views import (
    RateListView, NewListView, SaveListView,
    cardset_rate, cardset_search, cardset_save,
)

urlpatterns = [
    path('rate_list', RateListView.as_view(), name='rate_list'),
    path('new_list', NewListView.as_view(), name='new_list'),
    path('save_list', SaveListView.as_view(), name='save_list'),
    path('cardset/<int:pk>/rate', cardset_rate, name='cardset_rate'),
    path('search', cardset_search, name='cardset_search'),
    path('save', cardset_save, name='cardset_save'),
]
