from django import forms
from .models import Post, Category


# class NewsForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ['title', 'content', 'author', 'category']
#
# class ArticleForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ['title', 'content', 'author', 'category']

class PostChangeForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'author', 'categories']
        labels = {
            'title': 'Заголовок',
            'content': 'Содержание',
            'author': 'Автор',
            'categories': 'Категории'
        }





