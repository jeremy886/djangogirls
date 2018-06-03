from mysite import wsgi


def show_latest_post_title():
    from blog.models import Post

    post = Post.objects.latest('id')
    print(post)


def show_post_data(Post, message):
    print('-' * 40, message)
    posts = Post.objects.all()
    for post in posts:
        print(post, '---', post.viewed)


def add_all_post_viewed_by_count(count):
    from blog.models import Post
    from django.db.models import F

    show_post_data(Post, "BEFORE UPDATE")
    Post.objects.all().update(viewed=F('viewed')+count)
    show_post_data(Post, "AFTER UPDATE")



def double_viewed_count():
    from blog.models import Post
    from django.db.models import F

    show_post_data(Post, "BEFORE UPDATE")
    posts = Post.objects.all()
    posts.update(viewed=F("viewed")*2)
    show_post_data(Post, "AFTER UPDATE")


if __name__ == '__main__':

    # show_latest_post_title()
    # add_all_post_viewed_by_count(1)
    double_viewed_count()