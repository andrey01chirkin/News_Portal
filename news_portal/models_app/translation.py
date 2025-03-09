from .models import Post, Category
from modeltranslation.translator import register, TranslationOptions

# Перевод для категорий
@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', )  # Переводим только имя категории

# Перевод для статей
@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'content')  # Переводим заголовок и контент статьи