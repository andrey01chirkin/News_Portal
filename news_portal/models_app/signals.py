import os
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from dotenv import load_dotenv
from .models import Post, Author


@receiver(m2m_changed, sender=Post.categories.through)
def notify_subscribers(sender, instance, action, **kwargs):
    load_dotenv()
    if action == "post_add":
        categories = instance.categories.all()
        for category in categories:
            for subscriber in category.subscribers.all():
                send_mail(
                    subject=f"Новая новость в категории {category.name}",
                    message=f"Здравствуйте, {subscriber.username}!\
                        \nВ категории \"{category.name}\" появилась новая новость!\
                        \nЗаголовок: {instance.title}\
                        \nКраткое содержание: {instance.content[:50]}...\
                        \nhttp://127.0.0.1:8000/news/{instance.id}",
                    from_email=os.getenv('email'),
                    recipient_list=[subscriber.email],
                    fail_silently=False,
                )


