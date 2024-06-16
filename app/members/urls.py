from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import MemberCreate, MemberLogin, MemberLogout, CustomTokenObtainPairView

urlpatterns = [
    path('create/', MemberCreate.as_view(), name='member-create'),
    path('login/', MemberLogin.as_view(), name='member-login'),
    path('logout/', MemberLogout.as_view(), name='member-logout'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
