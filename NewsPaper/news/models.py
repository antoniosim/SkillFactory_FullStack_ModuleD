from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

article = 'AR'
newnews = 'NW'

CONTENT = [(article, 'Статья'), (newnews, 'Новость')]


class Author(models.Model):
    userID = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        self.rating = self.authorposts.all().aggregate(Sum('rating'))['rating__sum'] * 3
        self.rating += self.userID.usercomments.all().aggregate(Sum('rating'))['rating__sum']
        for q1 in self.authorposts.all():
            for q2 in q1.postcomments.exclude(userID=self.userID):
                self.rating += q2.rating
        self.save()
        return f'New rating = {self.rating}'


class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    authorID = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='authorposts')
    type = models.CharField(max_length=2, choices=CONTENT, default='NW')
    createdAt = models.DateTimeField(auto_now_add=True)
    heading = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField(default=0)
    categories = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.content[:124] + '...'


class Comment(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usercomments")
    postID = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="postcomments")
    content = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class PostCategory(models.Model):
    postID = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryID = models.ForeignKey(Category, on_delete=models.CASCADE)


def show_best_author():
    best_author = Author.objects.order_by("-rating")[0]
    print(f'Лучший автор: {best_author.userID.username}, рейтинг: {best_author.rating}')


def show_best_article(show_comments=False):
    best_article = Post.objects.order_by("-rating")[0]
    res = '\n\n' + f'"{best_article.heading}" [Рейтинг: {best_article.rating}]' + '\n' \
          f'{best_article.preview()}' + '\n' \
          f'{best_article.createdAt.strftime("%d.%m.%Y %H:%M:%S")} ({best_article.authorID.userID.username})' + '\n\n'

    if show_comments:
        for comt in best_article.postcomments.all():
            res += f'[{comt.createdAt.strftime("%d.%m.%Y %H:%M:%S")}] - {comt.userID.username}' + '\n' \
                   f'{comt.content}' + '\n' \
                   f'[Рейтинг: {comt.rating}]' + '\n\n'
    print(res)
