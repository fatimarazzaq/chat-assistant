from django.urls import path
from . import views


# Web URLs only
urlpatterns = [
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.user_profile, name='user-profile'),
    path('edit-profile/', views.user_edit_profile, name='user-edit-profile'),
    path('logout/', views.user_logout, name='logout'),
]

# API URLs
api_urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='api_register'),
    path('login/', views.LoginAPIView.as_view(), name='api_login'),
    path('logout/', views.LogoutAPIView.as_view(), name='api_logout'),
    path('profile/', views.UserProfileAPIView.as_view(), name='api_profile'),
    path('token/refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),
]

# Combine URLs based on the URL prefix
urlpatterns += api_urlpatterns
