from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
# Create your views here.
from django.utils import timezone
from .models import Chat
from fileupload.models import FaissIndex
from .chatsys import get_response
from django.contrib.auth.decorators import login_required
import re
import os



@login_required
def home(response):
    return render(response, "Aweapp/home.html", {"name": "Welcome to Awe!"})
def format_reply(reply):
  """
  Formats a string by replacing:
  - All '*' with '\n' (newline)
  - Double asterisks ('**') with HTML bold tags (<b> and </b>)
  """
  bold_pattern = r"\*\*([^*]+)\*\*"
  single_star_pattern = r"\*"

  # Replace bold sections
  formatted_text = re.sub(bold_pattern, r"<b>\1</b>", reply)

  # Replace single stars
  formatted_text = re.sub(single_star_pattern, r"<br>", formatted_text)

  # Ensure closing bold tag if necessary

  print(formatted_text)
  return formatted_text

def chat(response):
    # file_address = r"C:\Users\seq_amal\djnapp\dnapp_\Awe\Aweapp\static\images\generated_image.JPEG"  # Replace with the actual file path
    # if os.path.exists(file_address):
    #     os.remove(file_address)
    #     print(f"File at {file_address} has been deleted.")
    if response.method == 'POST':
        user = response.user
        index=FaissIndex.objects.filter(user=user).first()
        if not index:
            index = FaissIndex.objects.create(user=user)   #try get
        message = response.POST.get('message')
        reply = get_response(message, index)
        chat = Chat(message=message, response=reply, created_at=timezone.now)
        chat.save()
        reply = format_reply(reply)
        if reply.endswith('.JPEG'):
            print("Image reply:",reply)
            # return JsonResponse({'message': message,'imagepath':1})
            reply=""
        else:
            # Attempt to delete the file at the given address
            file_address = r"C:\Users\seq_amal\djnapp\dnapp_\Awe\Aweapp\static\images\generated_image.JPEG"  # Replace with the actual file path
            if os.path.exists(file_address):
                os.remove(file_address)
                print(f"File at {file_address} has been deleted.")
            else:
                print(f"File at {file_address} does not exist.")
        return JsonResponse({'message': message, 'response': reply})
    return render(response, 'Aweapp/chat.html', {})
def about(response):
    """Renders the about page using the Aweapp/about.html template."""
    return render(response, "Aweapp/about.html")
