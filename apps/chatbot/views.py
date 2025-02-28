from django.shortcuts import render
from django.http import JsonResponse
from openai import OpenAI
from django.conf import settings
from .models import Chat  # Import the Chat model
from django.contrib.auth.decorators import login_required  # To ensure the user is logged in

# Initialize OpenAI client
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

@login_required  # Ensure only authenticated users can chat
def chat(request):
    if request.method == "POST":
        user_message = request.POST.get("message", "")

        if user_message.strip():  # Ensure message is not empty
            bot_reply = chat_response(user_message)

            # Store chat in the database
            chat_entry = Chat.objects.create(
                user=request.user,
                message=user_message,
                response=bot_reply
            )

            return JsonResponse({"response": bot_reply})

    return render(request, "chatbot/chat.html")
