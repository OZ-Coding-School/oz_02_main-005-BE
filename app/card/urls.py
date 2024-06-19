from django.contrib import admin
from django.urls import path
from .views import CardView,CardUpdateView,CardGetView
urlpatterns = [
    path('create/<int:cardset_id>',CardView.as_view(),name='post'),
    path('update/<int:cardset_id>',CardUpdateView.as_view(),name='post'),
    path('each/<int:cardset_id>',CardGetView.as_view(),name='get')

]