from .models import Author, Post


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
