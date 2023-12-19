from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from .models import ToDoList, Item
from .forms import CreateNewChat
def home(response):
    return render(response, "Aweapp/home.html", {"name": "Welcome to Awe!"})
def index(response, id):
    ls= ToDoList.objects.get(id=id)
    return render( response, "Aweapp/index.html", {"name": ls.name , "posts":ls.item_set.all()})

def v1(response):
    return HttpResponse("<h1>Hello, world. You're at the Awe v1.</h1>")

def chat(response):
    """Renders the chat page using the Aweapp/chat.html template."""
    form = CreateNewChat()
    return render(response, "Aweapp/chat.html", {"form":form})
