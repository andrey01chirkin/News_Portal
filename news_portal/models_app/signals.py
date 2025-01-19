from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Post

@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if created and instance.post_type == Post.NEWS:
        categories = instance.categories.all()
        for category in categories:
            for subscriber in category.subscribers.all():
                send_mail(
                    subject=f"Новая новость в категории {category.name}",
                    message=f"""
                        Здравствуйте, {subscriber.username}.
                        В категории '{category.name}' появилась новая новость!
    
                        Заголовок: {instance.title}
                        Краткий текст: {instance.content[:50]}...
                        """,
                    from_email='some_email@gmail.com',
                    recipient_list=[subscriber.email],
                    fail_silently=False,
                )


