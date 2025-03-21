from django.core.cache import cache
from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='author')
    rating = models.IntegerField(default=0)

    def update_rating(self):
        # Суммарный рейтинг каждой статьи автора умножается на 3
        post_ratings = sum(post.rating * 3 for post in self.posts.all())

        # Суммарный рейтинг всех комментариев автора
        comment_ratings = sum(comment.rating for comment in self.user.comments.all())

        # Суммарный рейтинг всех комментариев к статьям автора
        comments_on_posts_ratings = sum(
            comment.rating for post in self.posts.all() for comment in post.comments.all()
        )

        self.rating = post_ratings + comment_ratings + comments_on_posts_ratings
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(User, related_name='subscribed_categories', blank=True)

    def __str__(self):
        return self.name.title()


class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'

    POST_TYPE_CHOICES = [
        (ARTICLE, 'Article'),
        (NEWS, 'News'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    post_type = models.CharField(max_length=2, choices=POST_TYPE_CHOICES, default=ARTICLE)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.content[:124]}...' if len(self.content) > 124 else self.content

    def __str__(self):
        return f'{self.title}: {self.content}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        if self.post_type == Post.ARTICLE:
            cache.delete(f'article-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


