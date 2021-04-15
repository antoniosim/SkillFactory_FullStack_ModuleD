from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

article = 'AR'
newnews = 'NW'

CONTENT = [(article, 'Статья'), (newnews, 'Новость')]


class Author(models.Model):
    userID = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def update_rating(self):
        articles_rating = self.objects.authorposts.all().aggregate(Sum('rating')) * 3
        # comments_rating = User.objects.get(id=self.userID).usercomments.all().aggregate(Sum('rating'))
        # feedback_rating = self.authorposts.all().postcomments.filter(comment__userID != self.userID).aggregate(
        #     Sum('rating'))
        self.rating = articles_rating #+ comments_rating + feedback_rating
        self.save()


class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    authorID = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="authorposts")
    type = models.CharField(max_length=2, choices=CONTENT, default=newnews)
    createdAt = models.DateTimeField(auto_now_add=True)
    heading = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField()
    categories = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1

    def dislike(self):
        self.rating -= 1

    def preview(self):
        return self.content[:124] + '...'


class PostCategory(models.Model):
    postID = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryID = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usercomments")
    postID = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="postcomments")
    content = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField()

    def like(self):
        self.rating += 1

    def dislike(self):
        self.rating -= 1
