from django.db import models

# Create your models here.
class ToDoList(models.Model):
    name= models.CharField(max_length=200)

    def __str__(self):
        return self.name
class Item(models.Model):
    todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    complete = models.BooleanField()

    def __str__(self):
        return self.text
class Chat(models.Model):
    
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.message}'