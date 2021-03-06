# Generated by Django 3.2 on 2021-04-15 19:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('userID', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('AR', 'Статья'), ('NW', 'Новость')], default='NW', max_length=2)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('heading', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('rating', models.IntegerField()),
                ('authorID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authorposts', to='news.author')),
            ],
        ),
        migrations.CreateModel(
            name='PostCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoryID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.category')),
                ('postID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.post')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='categories',
            field=models.ManyToManyField(through='news.PostCategory', to='news.Category'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('rating', models.IntegerField()),
                ('postID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postcomments', to='news.post')),
                ('userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usercomments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
