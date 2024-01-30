from django.shortcuts import render
from .forms import FileForm
from Aweapp.chatsys import extract_text_from_file
from .models import FaissIndex
import uuid
# Create your views here.
def fileupload(response):
    message="please upload a file to be indexed"
    if response.method== 'POST':
        form = FileForm(response.POST, response.FILES)

        if form.is_valid():
            form.save()
            uploaded_file = form.instance

            # Get the file path
            file_path = uploaded_file.file.path

            # Print a message about the file path
            print("File saved at:", file_path)

            text=extract_text_from_file(file_path)
            user=response.user
            print("text extracted")

            # Generate a unique index_id composed of the user's username and the file name
            index_id = f"{user.username}_{uploaded_file.name}_{uuid.uuid4()}"
            index = FaissIndex.objects.filter(user=user).order_by('-id').first()
            index.index_id=index_id
            index.user=user
            print(text)
            
            try:
                index.add_to_index(text)

                print("index created")
                message = "Index saved successfully."
                index.save()
            except Exception as e:
                print(f"Error saving index: {e}")
                message= "Error saving index."
            return render(response, 'fileupload/fileupload.html', {'form':form, 'message': message})
    context={'form':FileForm(), 'message': message}
    return render(response, 'fileupload/fileupload.html', context)

def display_upindex(response):
    """
    This function displays the UpIndex.html page for the current user,
    passing the context of the index object of FaissIndex.
    """
    user = response.user
    indexes = FaissIndex.objects.filter(user=user)
    context = {'indexes': indexes}
    return render(response, 'fileupload/UpIndex.html', context)
