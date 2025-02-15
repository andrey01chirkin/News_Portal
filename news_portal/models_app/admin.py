from django.contrib import admin
from models_app.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'rating')
    list_filter = ('post_type',)
    search_fields = ('title', 'content')


admin.site.register(Post, PostAdmin)
