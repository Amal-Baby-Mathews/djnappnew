from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegisterForm
from fileupload.models import FaissIndex
# Create your views here.
def register(response):
    if response.method == "POST":
        form=RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            username = form['username']
            FaissIndex.objects.create(user=username, index_id="shared_index")
        return redirect("/")
    else:
        form= RegisterForm()

    form= RegisterForm()
    return render(response, "register/register.html", {"form": form})