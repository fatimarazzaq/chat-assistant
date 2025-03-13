from rest_framework import serializers
from .models import ChatSession, Chat

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'message', 'response', 'created_at']
        read_only_fields = ['created_at']

class ChatSessionSerializer(serializers.ModelSerializer):
    chats = ChatSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatSession
        fields = ['id', 'title', 'created_at', 'chats', 'last_message']
        read_only_fields = ['created_at']

    def get_last_message(self, obj):
        last_chat = obj.chat_set.order_by('-created_at').first()
        if last_chat:
            return {
                'message': last_chat.message,
                'response': last_chat.response,
                'created_at': last_chat.created_at
            }
        return None

class ChatCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['message']

class ChatResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['response'] 