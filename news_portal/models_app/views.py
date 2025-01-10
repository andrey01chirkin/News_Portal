from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from .filters import NewsFilter
from .forms import PostChangeForm
from .models import Post


class NewsList(ListView):
    model = Post
    queryset = Post.objects.filter(post_type='NW').order_by('-created_at')
    template_name = 'news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10


class NewsDetail(DetailView):
    model = Post
    queryset = Post.objects.filter(post_type='NW')
    template_name = 'news_item.html'
    context_object_name = 'news_item'


class NewsListSearch(ListView):
    model = Post
    template_name = 'news_list_search.html'
    context_object_name = 'news_list'
    paginate_by = 10

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        queryset = Post.objects.filter(post_type='NW').order_by('-created_at')
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


# Представления для новостей (News):
class NewsCreateView(CreateView):
    model = Post
    form_class = PostChangeForm
    template_name = 'news_create.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        form.instance.post_type = Post.NEWS  # Устанавливаем тип как News
        return super().form_valid(form)


class NewsUpdateView(UpdateView):
    model = Post
    form_class = PostChangeForm
    template_name = 'news_edit.html'
    success_url = reverse_lazy('news_list')

    def get_queryset(self):
        return Post.objects.filter(post_type=Post.NEWS)  # Фильтруем только новости


class NewsDeleteView(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')

    def get_queryset(self):
        return Post.objects.filter(post_type=Post.NEWS)  # Фильтруем только новости


# Представления для статей (Articles)
class ArticleCreateView(CreateView):
    model = Post
    form_class = PostChangeForm
    template_name = 'article_create.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        form.instance.post_type = Post.ARTICLE  # Устанавливаем тип как Article
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostChangeForm
    template_name = 'article_edit.html'
    success_url = reverse_lazy('news_list')

    def get_queryset(self):
        return Post.objects.filter(post_type=Post.ARTICLE)  # Фильтруем только статьи


class ArticleDeleteView(DeleteView):
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('news_list')

    def get_queryset(self):
        return Post.objects.filter(post_type=Post.ARTICLE)  # Фильтруем только статьи
