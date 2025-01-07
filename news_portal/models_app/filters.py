from datetime import timedelta
import django_filters
from django.forms import DateInput
from django_filters import FilterSet
from .models import Post

class NewsFilter(FilterSet):
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='iregex',
        label='По заголовку'
    )
    author = django_filters.CharFilter(
        field_name='author__user__first_name',
        lookup_expr='iregex',
        label='По имени автора'
    )
    created_at = django_filters.DateFilter(
        field_name='created_at',
        method='filter_by_date',
        label='Позже даты',
        widget=DateInput(attrs={'type': 'date'})
    )

    def filter_by_date(self, queryset, name, value):
        """
        Фильтруем записи с временем, исключая указанную дату.
        """
        next_day = value + timedelta(days=1)  # Увеличиваем дату на 1 день
        return queryset.filter(created_at__gte=next_day)

    class Meta:
        model = Post
        fields = ['title', 'author', 'created_at']



