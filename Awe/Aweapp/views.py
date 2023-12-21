from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.
from django.utils import timezone
from .models import ToDoList, Item, Chat
from .forms import CreateNewChat
from .chatsys import get_response
from django.contrib.auth.decorators import login_required

@login_required
def home(response):
    return render(response, "Aweapp/home.html", {"name": "Welcome to Awe!"})


def chat(response):
    if response.method == 'POST':
        message = response.POST.get('message')
        reply = get_response(message)

        chat = Chat(message=message, response=reply, created_at=timezone.now)
        chat.save()
        return JsonResponse({'message': message, 'response': reply})
    return render(response, 'Aweapp/chat.html', {})
def about(response):
    """Renders the about page using the Aweapp/about.html template."""
    return render(response, "Aweapp/about.html")
