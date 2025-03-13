from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='api_register'),
    path('login/', views.LoginAPIView.as_view(), name='api_login'),
    path('logout/', views.LogoutAPIView.as_view(), name='api_logout'),
    path('profile/', views.UserProfileAPIView.as_view(), name='api_profile'),
    path('token/refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),
] 