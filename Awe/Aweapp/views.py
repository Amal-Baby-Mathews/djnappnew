from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.
from django.utils import timezone
from .models import ToDoList, Item, Chat
from .forms import CreateNewChat
from .chatsys import get_response
def home(response):
    return render(response, "Aweapp/home.html", {"name": "Welcome to Awe!"})
def index(response, id):
    ls= ToDoList.objects.get(id=id)
    return render( response, "Aweapp/index.html", {"name": ls.name , "posts":ls.item_set.all()})

def v1(response):
    return HttpResponse("<h1>Hello, world. You're at the Awe v1.</h1>")

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
