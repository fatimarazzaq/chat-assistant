from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router for API endpoints
router = DefaultRouter()
router.register(r'sessions', views.ChatSessionViewSet, basename='chat-session')
router.register(r'sessions/(?P<session_pk>[^/.]+)/chats', views.ChatViewSet, basename='chat')

urlpatterns = [
    path('', include(router.urls)),
] 