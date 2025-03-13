from django.urls import path
from . import views

# Web URLs only
urlpatterns = [
    path('', views.chat, name='chat_home'),
    path('chat/session/create/', views.create_chat_session, name='create_chat_session'),
    path('chat/session/<uuid:session_id>/rename/', views.rename_chat_session, name='rename_chat_session'),
    path('chat/session/<uuid:session_id>/delete/', views.delete_chat_session, name='delete_chat_session'),
    path('load_session/<uuid:session_id>/', views.load_chat_session, name='load_chat_session'),
    path('chat/<uuid:session_id>/', views.chat_session_view, name='chat_session'),
]
