from django.contrib import admin
from .models import Post
from modeltranslation.admin import TranslationAdmin
from models_app.models import Category


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'rating')
    list_filter = ('post_type',)
    search_fields = ('title', 'content')

# Добавляем поддержку перевода в админку
class CategoryAdmin(TranslationAdmin):
    model = Category

class PostAdmin(TranslationAdmin):
    model = Post


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
