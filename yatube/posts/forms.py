from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')
        labels = {
            'text': 'Введите текст',
            'group': 'Выберите группу'
        }
        help_text = {
            'text': 'Любую абракадабру',
            'group': 'Из уже существующих'
        }
