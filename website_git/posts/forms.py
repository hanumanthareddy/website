from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "image"
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Blog Title','minlength':'10','maxlength':'120','class': 'form-control col-9'}),
            'content': forms.Textarea(attrs={'placeholder': 'Blog Content ','minlength':'120','class': 'form-control col-9'}),
            # 'image': forms.ClearableFileInput(attrs={'multiple': True})
            'image': forms.ClearableFileInput()
        }
        labels = {
               'title': '',
               'content': '',
               'image': 'Upload a Suitable Image '
        }