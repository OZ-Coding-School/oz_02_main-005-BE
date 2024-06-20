from django.contrib import admin
from django.urls import path
from .views import CardSetView,CardSetSaveView,CardSetGetView
urlpatterns = [
    path('create',CardSetView.as_view(),name='post'),
    path('mainlist',CardSetView.as_view(),name='get'),
    path('savelist/<int:member_id>',CardSetSaveView.as_view(),name='get'),
    path('update/<int:cardset_id>',CardSetSaveView.as_view(),name='post'),
    path('recent/<int:member_id>',CardSetGetView.as_view(),name='get')
]