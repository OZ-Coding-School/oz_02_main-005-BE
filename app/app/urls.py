from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from members.views import home
urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path('cardset/',include('cardset.urls')),
    path('cards/',include('card.urls')),
    path("folders/", include("folders.urls")),
    path("comments/", include("comments.urls")),
    
    path("member/", include("members.urls")),
    path('accounts/', include('allauth.urls')),
    path('community/', include('community.urls')),]