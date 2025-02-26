from django.shortcuts import render
from django.http import JsonResponse
from openai import OpenAI

# Create your views here.

api_key="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"

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

def chat(request):
    if request.method == "POST":
        user_message = request.POST.get("message", "")
        bot_reply = chat_response(user_message)
        return JsonResponse({"response": bot_reply})

    return render(request, "chatbot/chat.html")
