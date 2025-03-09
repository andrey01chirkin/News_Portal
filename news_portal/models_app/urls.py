from django.urls import path
from django.views.decorators.cache import cache_page

from .views import NewsList, NewsDetail, NewsListSearch, NewsCreateView, NewsUpdateView, NewsDeleteView, \
    ArticleCreateView, ArticleUpdateView, ArticleDeleteView, ArticleDetail

urlpatterns = [
    # Новости
    # path('news/', cache_page(60)(NewsList.as_view()), name='news_list'),
    path('news/', NewsList.as_view(), name='news_list'),
    # path('news/<int:pk>/', cache_page(60*5)(NewsDetail.as_view()), name='news_by_id'),
    path('news/<int:pk>/', NewsDetail.as_view(), name='news_by_id'),

    path('news/search/', NewsListSearch.as_view(), name='news_search'),

    path('news/create/', NewsCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', NewsUpdateView.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    # Статьи
    path('article/<int:pk>/', ArticleDetail.as_view(), name='article_by_id'),
    path('article/create/', ArticleCreateView.as_view(), name='article_create'),
    path('article/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'),
    path('article/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
]


