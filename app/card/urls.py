from django.contrib import admin
from django.urls import path
from .views import CardView
urlpatterns = [
    path('create',CardView.as_view(),name='post'),
    path('update',CardView.as_view(),name='update'),

]