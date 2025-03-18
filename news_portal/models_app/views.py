from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from .filters import NewsFilter
from .forms import PostChangeForm
from .models import Post, Author
from celery_app.tasks import create_news_celery
from django.utils import timezone
import pytz
from rest_framework import viewsets, permissions
from .serializers import NewsSerializer, ArticleSerializer

class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """Разрешает GET, HEAD, OPTIONS всем, а POST, PUT, DELETE — только авторизованным пользователям."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
        return request.user and request.user.is_authenticated


class NewsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(post_type='NW').order_by('-created_at')
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(post_type='AR').order_by('-created_at')
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# ----------------------------------------------------------------------------

class NewsList(ListView):
    model = Post
    queryset = Post.objects.filter(post_type='NW').order_by('-created_at')
    template_name = 'news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем часовой пояс из сессии
        tzname = self.request.session.get('django_timezone', 'Europe/Moscow')
        user_tz = pytz.timezone(tzname)

        # Локализуем текущее время
        current_time = timezone.now().astimezone(user_tz)

        # Передаём данные в шаблон
        context['current_time'] = current_time
        context['current_hour'] = current_time.hour
        context['timezones'] = pytz.common_timezones
        context['selected_timezone'] = tzname  # Передаём выбранный часовой пояс

        return context

    def post(self, request):
        """Обрабатываем смену часового пояса."""
        request.session['django_timezone'] = request.POST.get('timezone', 'Europe/Moscow')
        return redirect('news_list')  # Перенаправляем пользователя обратно на список новостей


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
        # Проверка количества новостей пользователя за текущий день
        today = now().date()
        news_today = Post.objects.filter(
            author=self.request.user.author,
            post_type=Post.NEWS,
            created_at__date=today
        ).count()

        if news_today >= 3:
            # Добавляем сообщение об ошибке и возвращаем пользователя на страницу
            messages.error(self.request, 'Вы не можете публиковать более 3 новостей в сутки.')
            return redirect('/accounts/')

        form.instance.author = Author.objects.get(user=self.request.user)
        form.instance.post_type = Post.NEWS
        instance = form.save()

        create_news_celery.delay(instance.pk)
        return super().form_valid(form)


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


class ArticleDetail(DetailView):
    model = Post
    queryset = Post.objects.filter(post_type='AR')
    template_name = 'news_item.html'
    context_object_name = 'news_item'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'article-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'article-{self.kwargs["pk"]}', obj)

        return obj


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
