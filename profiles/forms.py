from django import forms

class PostFrom(forms.Form):
    text = forms.CharField(label="Description")
    image = forms.FileField()