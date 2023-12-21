from django.shortcuts import render

# Create your views here.
def fileupload(response):
    return render(response, 'fileupload/fileupload.html', {})