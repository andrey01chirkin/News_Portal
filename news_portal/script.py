import os
import django

# Укажите путь к вашему проекту
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_portal.settings')

# Инициализируйте Django
django.setup()

# Импортируйте вашу модель
from models_app.models import *

User.objects.all().delete()
Author.objects.all().delete()
Category.objects.all().delete()
Comment.objects.all().delete()
Post.objects.all().delete()
Post.objects.all().delete()


# 1. Создать двух пользователей
user1 = User.objects.create_user(username='user1', password='password1')
user2 = User.objects.create_user(username='user2', password='password2')

# 2. Создать два объекта модели Author
author1 = Author.objects.create(user=user1)
author2 = Author.objects.create(user=user2)

# 3. Добавить 4 категории
category1 = Category.objects.create(name='Sport')
category2 = Category.objects.create(name='Politics')
category3 = Category.objects.create(name='Education')
category4 = Category.objects.create(name='Technology')

# 4. Добавить 2 статьи и 1 новость
post1 = Post.objects.create(author=author1, post_type='AR', title='Article 1', content='This is the content of Article 1.')
post2 = Post.objects.create(author=author1, post_type='AR', title='Article 2', content='This is the content of Article 2.')
news1 = Post.objects.create(author=author2, post_type='NW', title='News 1', content='This is the content of News 1.')

# 5. Присвоить категории статьям и новостям
post1.categories.add(category1, category2)
post2.categories.add(category3)
news1.categories.add(category2, category4)

# 6. Создать комментарии
comment1 = Comment.objects.create(post=post1, user=user1, content='Great article!')
comment2 = Comment.objects.create(post=post1, user=user2, content='I disagree with this article.')
comment3 = Comment.objects.create(post=post2, user=user1, content='Very informative.')
comment4 = Comment.objects.create(post=news1, user=user2, content='Interesting news_portal_app.')

# 7. Применить like() и dislike() для корректировки рейтингов
post1.like()
post1.like()
post2.like()
post2.dislike()
news1.like()

comment1.like()
comment1.like()
comment2.dislike()
comment3.like()
comment4.dislike()

# 8. Обновить рейтинги пользователей
author1.update_rating()
author2.update_rating()

# 9. Вывести username и рейтинг лучшего пользователя
best_author = Author.objects.order_by('-rating').first()
print(f"Best Author: {best_author.user.username}, Rating: {best_author.rating}")

# 10. Вывести информацию о лучшей статье
best_post = Post.objects.order_by('-rating').first()
print(f"Best Post:\n"
      f"Date: {best_post.created_at}\n"
      f"Author: {best_post.author.user.username}\n"
      f"Rating: {best_post.rating}\n"
      f"Title: {best_post.title}\n"
      f"Preview: {best_post.preview()}")

# 11. Вывести все комментарии к лучшей статье
comments = best_post.comments.all()
for comment in comments:
    print(f"Date: {comment.created_at}, User: {comment.user.username}, Rating: {comment.rating}, content: {comment.content}")
