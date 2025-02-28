from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from openai import OpenAI
from django.conf import settings
from .models import Chat, ChatSession
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json

api_key = settings.OPENAI_API_KEY
client = OpenAI(api_key=api_key)

def chat_response(message):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message},
        ]
    )
    return completion.choices[0].message.content

@login_required
def chat(request, session_id=None):
    """Handles the chat view with session persistence"""
    chat_sessions = ChatSession.objects.filter(user=request.user).order_by("-created_at")
    chat_session = None
    chats = []

    if session_id:
        chat_session = get_object_or_404(ChatSession, id=session_id, user=request.user)
    elif chat_sessions.exists():
        chat_session = chat_sessions.first()  # Load latest session if none selected
    else:
        chat_session = ChatSession.objects.create(user=request.user, title="New Chat Session")

    if chat_session:
        chats = Chat.objects.filter(chat_session=chat_session).order_by("created_at")

    if request.method == "POST":
        user_message = request.POST.get("message", "").strip()
        if user_message:
            bot_reply = chat_response(user_message)
            Chat.objects.create(chat_session=chat_session, message=user_message, response=bot_reply)
            return JsonResponse({"response": bot_reply, "session_id": str(chat_session.id)})

    return render(request, "chatbot/chat.html", {
        "chat_sessions": chat_sessions,
        "chats": chats,
        "selected_session": chat_session,  # Ensure selected session is loaded
    })

@login_required
def load_chat_session(request, session_id):
    """Loads a specific chat session and returns its messages"""
    chat_session = get_object_or_404(ChatSession, id=session_id, user=request.user)
    chats = [
        {"message": chat.message, "response": chat.response} 
        for chat in chat_session.chat_set.all().order_by("created_at")
    ]
    return JsonResponse({"chats": chats})

@csrf_exempt
@login_required
def create_chat_session(request):
    """Creates a new chat session for the logged-in user"""
    if request.method == "POST":
        session = ChatSession.objects.create(title="New Chat", user=request.user)
        return JsonResponse({
            "success": True,
            "session_id": str(session.id),
            "session_title": session.title
        })
    return JsonResponse({"success": False}, status=400)

@csrf_exempt
@login_required
def rename_chat_session(request, session_id):
    """Renames an existing chat session"""
    if request.method == "POST":
        try:
            session = ChatSession.objects.get(id=session_id, user=request.user)
            data = json.loads(request.body)
            session.title = data.get("title", session.title)
            session.save()
            return JsonResponse({"success": True})
        except ChatSession.DoesNotExist:
            return JsonResponse({"success": False, "error": "Session not found"}, status=404)
    return JsonResponse({"success": False}, status=400)

@csrf_exempt
def delete_chat_session(request, session_id):
    print(session_id)
    if request.method == "DELETE":
        session = get_object_or_404(ChatSession, id=session_id)
        session.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)


@login_required
def chat_session_view(request, session_id):
    """Loads a chat session and renders the chat page"""
    session = get_object_or_404(ChatSession, id=session_id, user=request.user)
    return render(request, "chatbot/chat.html", {"chat_session": session})
