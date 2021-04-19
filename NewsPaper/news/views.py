from django.views.generic import ListView, DetailView  # импортируем класс получения деталей объекта
from .models import Post, Comment, Author


class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'


# создаём представление в котором будет детали конкретного отдельного товара
class PostDetail(DetailView):
    model = Post  # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    template_name = 'post.html'  # название шаблона будет product.html
    context_object_name = 'post'  # название объекта. в нём будет
