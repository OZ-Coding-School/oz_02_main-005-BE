from django.contrib import admin
from django.urls import path
from .views import CardSetView
urlpatterns = [
    path('create',CardSetView.as_view(),name='post'),
    path('mainlist',CardSetView.as_view(),name='get'),
    path('savelist',CardSetView.as_view(),name='getSave'),
    path('update',CardSetView.as_view(),name='udpate')
]