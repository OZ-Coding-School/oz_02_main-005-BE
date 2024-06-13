from django.urls import path
from .views import (
    RateListView, NewListView, SaveListView, CardsetDetailView,
    cardset_rate, cardset_search, cardset_save,
)

urlpatterns = [
    path('community/rate_list/', RateListView.as_view(), name='rate_list'),
    path('community/new_list/', NewListView.as_view(), name='new_list'),
    path('community/save_list/', SaveListView.as_view(), name='save_list'),
    path('community/cardset/<int:pk>/', CardsetDetailView.as_view(), name='cardset_public'),
    path('community/cardset/<int:pk>/rate/', cardset_rate, name='cardset_rate'),
    path('community/search/', cardset_search, name='cardset_search'),
    path('community/save/', cardset_save, name='cardset_save'),
]
