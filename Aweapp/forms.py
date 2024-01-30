from django import forms

class CreateNewChat(forms.Form):
    prompt = forms.CharField(label="Prompt", max_length=100)
    check= forms.BooleanField()
    