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

    def __str__(self):
        return f'{self.userID.last_name} {self.userID.first_name}'


class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'#{self.title.upper()}'


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

    def __str__(self):
        return f'{self.pk}: [{self.authorID.userID.last_name} {self.authorID.userID.first_name}] {self.heading}'


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

    def __str__(self):
        return f'{self.content[:100]}'


class PostCategory(models.Model):
    postID = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryID = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'[#{self.categoryID.title.upper()}] {self.postID.heading}'