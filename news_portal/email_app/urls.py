from django.urls import path
from .views import SubscribeToCategoryView


urlpatterns = [
    path('category/<int:pk>/', SubscribeToCategoryView.as_view(), name='category_detail'),
]
