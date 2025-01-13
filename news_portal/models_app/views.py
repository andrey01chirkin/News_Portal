from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from .filters import NewsFilter
from .forms import PostChangeForm
from .models import Post, Category


class NewsList(ListView):
    model = Post
    queryset = Post.objects.filter(post_type='NW').order_by('-created_at')
    template_name = 'news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_premium'] = not self.request.user.groups.filter(name='authors').exists()
        return context


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
class NewsCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('models_app.add_post',)

    model = Post
    form_class = PostChangeForm
    template_name = 'news_create.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        form.instance.post_type = Post.NEWS  # Устанавливаем тип как News
        response = super().form_valid(form)

        # Рассылка подписчикам категорий
        categories = form.cleaned_data.get('categories')  # Выбранные категории
        post = form.instance  # Сохранённый пост

        for category in categories:
            for subscriber in category.subscribers.all():
                send_mail(
                    subject=post.title,
                    message=f"""
                            Здравствуй, {subscriber.username}. 
                            Новая статья в твоём любимом разделе: {category.name}!

                            Заголовок: {post.title}
                            Краткий текст: {post.content[:50]}
                            """,
                    from_email='chirkin.extra@yandex.ru',
                    recipient_list=[subscriber.email],
                    fail_silently=False,
                )
        return response


class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('models_app.change_post',)

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
class ArticleCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('models_app.add_post',)

    model = Post
    form_class = PostChangeForm
    template_name = 'article_create.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        form.instance.post_type = Post.ARTICLE  # Устанавливаем тип как Article
        return super().form_valid(form)


class ArticleUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('models_app.change_post',)

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


@login_required
def subscribe_to_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.subscribers.add(request.user)
    return redirect('/news/', category_id=category_id)