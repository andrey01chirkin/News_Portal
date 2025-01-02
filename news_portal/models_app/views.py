from django.views.generic import ListView, DetailView
from .models import Post


class NewsList(ListView):
    model = Post
    queryset = Post.objects.filter(post_type='NW').order_by('-created_at')
    template_name = 'news_list.html'
    context_object_name = 'news_list'


class NewsDetail(DetailView):
    model = Post
    queryset = Post.objects.filter(post_type='NW')
    template_name = 'news_item.html'
    context_object_name = 'news_item'
