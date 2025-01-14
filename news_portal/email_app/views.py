from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView
from models_app.models import Category
from models_app.models import Post


class SubscribeToCategoryView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'email_app/subscribe_category.html'
    context_object_name = 'category'

    def post(self, request, *args, **kwargs):
        """Обработка подписки на категорию"""
        category = self.get_object()
        if not category.subscribers.filter(id=request.user.id).exists():
            category.subscribers.add(request.user)  # Добавляем текущего пользователя в подписчики
        return render(request, 'email_app/subscribe_congratulation.html', {'category': category})

    def get_context_data(self, **kwargs):
        """Добавляем в контекст только новости, связанные с категорией"""
        context = super().get_context_data(**kwargs)
        category = self.get_object()

        context['news'] = category.posts.filter(post_type=Post.NEWS)
        context['is_subscribed'] = category.subscribers.filter(id=self.request.user.id).exists()
        return context


