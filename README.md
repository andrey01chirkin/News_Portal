# Страницы
- /about/
- /contacts/
- /static_page_1/ - используется шаблон default.html
- /static_page_2/ - используется шаблон static_page_2.html
- /static_page_3/ - используется шаблон static_page_3.html. Страница доступна только администратору.
- /news - отображает список новостей в виде таблицы в шаблоне news_list.html
- /news/id - отображает новость по id из БД в шаблоне news_item.html
- /news/create/ - создает новость
- /news/<int:pk>/edit/ - редактирует новость
- /news/<int:pk>/delete/ - удаляет новость
- /articles/create/ - создает статью
- /articles/<int:pk>/edit/ - редактирует статью
- /articles/<int:pk>/delete/ - удаляет статью
