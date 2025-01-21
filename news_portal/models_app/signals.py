from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Post, Author


@receiver(m2m_changed, sender=Post.categories.through)
def notify_subscribers(sender, instance, action, **kwargs):
    if action == "post_add":
        categories = instance.categories.all()
        for category in categories:
            for subscriber in category.subscribers.all():
                send_mail(
                    subject=f"Новая новость в категории {category.name}",
                    message=f"Здравствуйте, {subscriber.username}!\
                        \nВ категории \"{category.name}\" появилась новая новость!\
                        \nЗаголовок: {instance.title}\
                        \nКраткое содержание: {instance.content[:50]}...",
                    from_email='chirkin.andrey377@gmail.com',
                    recipient_list=[subscriber.email],
                    fail_silently=False,
                )


