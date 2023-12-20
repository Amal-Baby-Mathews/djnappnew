from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from .models import ToDoList, Item
from .forms import CreateNewChat
from .chatsys import get_response
def home(response):
    return render(response, "Aweapp/home.html", {"name": "Welcome to Awe!"})
def index(response, id):
    ls= ToDoList.objects.get(id=id)
    return render( response, "Aweapp/index.html", {"name": ls.name , "posts":ls.item_set.all()})

def v1(response):
    return HttpResponse("<h1>Hello, world. You're at the Awe v1.</h1>")
messages = []
user_input=[]
def chat(response):
    global  message, user_input
    """Renders the chat page using the Aweapp/chat.html template."""
    if response.method == "POST":
        message = response.POST.get('message', '')
        
        out= get_response(message)
        p=[message,out]
        if p:
            user_input.append(p[0])
            messages.append(p)
        return render(response, "Aweapp/chat.html",  {"messages": messages, "user_input": user_input})
    else:
        form = CreateNewChat()
        return render(response, "Aweapp/chat.html", { "form": form})
def about(response):
    """Renders the about page using the Aweapp/about.html template."""
    return render(response, "Aweapp/about.html")
