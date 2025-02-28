from django.urls import path
from .views import *

urlpatterns = [
    path('', chat,name="chat_home"),
    path("chat/session/create/", create_chat_session, name="create_chat_session"),
    path("load_session/<uuid:session_id>/", load_chat_session, name="load_chat_session"),
    path("chat/session/<uuid:session_id>/rename/", rename_chat_session, name="rename_chat_session"),
    path("chat/session/<uuid:session_id>/delete/", delete_chat_session, name="delete_chat_session"),
    path('chat/<uuid:session_id>/', chat_session_view, name='chat_session'),


]
