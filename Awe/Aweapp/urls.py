from django.urls import path, include
from register import views as v
from fileupload import views as f
from . import   views
urlpatterns= [
  path("", views.home, name="home"),
  path("chat/", views.chat, name="chat"),
  path("about/", views.about, name="about"),
  path("register/", v.register, name="register"),
  path("", include("django.contrib.auth.urls")),
  path("fileupload/", f.fileupload, name="fileupload"),
  path("UpIndex/", f.display_upindex, name="UpIndex"),
]