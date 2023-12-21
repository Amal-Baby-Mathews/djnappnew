from django.shortcuts import render
from .forms import FileForm
# Create your views here.
def fileupload(response):
    if response.method== 'POST':
        form = FileForm(response.POST, response.FILES)
        if form.is_valid():
            form.save()
            return render(response, 'fileupload/fileupload.html', {'form':form})
    context={'form':FileForm()}
    return render(response, 'fileupload/fileupload.html', context)