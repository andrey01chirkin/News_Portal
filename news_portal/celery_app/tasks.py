import os
from datetime import timedelta
from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now
from models_app.models import Category, Post


@shared_task
def send_email_task(subject, message, recipient_list):
    send_mail(
        subject=subject,
        message=message,
        from_email=os.getenv('email'),
        recipient_list=recipient_list,
        fail_silently=False,
    )


@shared_task
def send_weekly_news():
    categories = Category.objects.all()
    last_week = now() - timedelta(days=7)
    for category in categories:
        posts = Post.objects.filter(categories=category, created_at__gte=last_week)
        if posts.exists():
            for subscriber in category.subscribers.all():
                message = "Еженедельная подборка новостей:\n"
                for post in posts:
                    message += f"{post.title}\n{post.content[:50]}...\nhttp://127.0.0.1:8000/news/{post.id}\n\n"
                send_email_task.delay(
                    subject=f"Еженедельная рассылка новостей в категории {category.name}",
                    message=message,
                    recipient_list=[subscriber.email]
                )