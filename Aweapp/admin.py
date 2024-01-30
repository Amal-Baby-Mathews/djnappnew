from django.contrib import admin

# Register your models here.
from .models import ToDoList
from .models import Item
admin.site.register(ToDoList)
admin.site.register(Item)
