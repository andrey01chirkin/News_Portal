import os
from datetime import timedelta
from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now
from dotenv import load_dotenv
from models_app.models import Category, Post


@shared_task
def create_news_celery(pk):
    """ Отправка уведомлений подписчикам категорий """
    load_dotenv()
    post = Post.objects.get(pk=pk)
    categories = post.categories.all()
    for category in categories:
        for subscriber in category.subscribers.all():
            send_mail(
                subject=f"Новая новость в категории {category.name}",
                message=f"Здравствуйте, {subscriber.username}!\
                            \nВ категории \"{category.name}\" появилась новая новость!\
                            \nЗаголовок: {post.title}\
                            \nКраткое содержание: {post.content[:50]}...\
                            \nhttp://127.0.0.1:8000/news/{post.id}",
                from_email=os.getenv('email'),
                recipient_list=[subscriber.email],
                fail_silently=False,
            )


@shared_task
def send_weekly_news():
    """ Еженедельная отправка новостей в категории подписчикам"""
    load_dotenv()
    one_week_ago = now() - timedelta(days=7)
    categories = Category.objects.all()
    for category in categories:
        subscribers_emails = list(category.subscribers.values_list('email', flat=True))
        news = Post.objects.filter(
            categories=category,
            created_at__gte=one_week_ago
        )
        if news.exists():
            news_content = "\n".join([f"{post.title}\n{post.content[:50]}...\nhttp://127.0.0.1:8000/news/{post.id}\n" for post in news])
            for email in subscribers_emails:
                send_mail(
                    subject=f"Еженедельная подборка новостей в категории {category.name}",
                    message=f"Здравствуйте!\nВот новости за прошедшую неделю:\n{news_content}",
                    from_email=os.getenv('email'),
                    recipient_list=[email],
                    fail_silently=False,
                )
