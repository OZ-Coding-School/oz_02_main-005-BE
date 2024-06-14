from django.contrib import admin
from django.urls import path
from .views import CardView
urlpatterns = [
    path('create/<int:cardset_id>',CardView.as_view(),name='post'),
    path('update/<int:cardset_id>',CardView.as_view(),name='update'),
    path('list/<int:cardset_id>',CardView.as_view(),name='get_cardset_card')

]