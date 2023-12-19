from django.urls import path

from . import   views
urlpatterns= [
  path("<int:id>/", views.index, name="index"), 
  path("v1/", views.v1, name="v1"), 
  path("", views.home, name="home"),
  path("chat/", views.chat, name="chat"),
  path("about/", views.about, name="about"),
]