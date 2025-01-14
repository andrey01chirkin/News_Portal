from django.urls import path
from .views import NewsList, NewsDetail, NewsListSearch, NewsCreateView, NewsUpdateView, NewsDeleteView, \
    ArticleCreateView, ArticleUpdateView, ArticleDeleteView, subscribe_to_category

urlpatterns = [
    # Новости
    path('news/', NewsList.as_view(), name='news_list'),
    path('news/<int:pk>', NewsDetail.as_view(), name='news_by_id'),

    path('news/search/', NewsListSearch.as_view(), name='news_search'),

    path('news/create/', NewsCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', NewsUpdateView.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    # Статьи
    path('articles/create/', ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),

    path('subscribe/<int:category_id>/', subscribe_to_category, name='subscribe_to_category'),

]
