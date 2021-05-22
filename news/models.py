from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _


class Author(models.Model):
    name = models.CharField(max_length=80)
    surname = models.CharField(max_length=160, blank=True)
    job_title = models.CharField(max_length=160, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return str(self.name) + ' ' + str(self.surname)

    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.id)])


def get_deleted_author():
    return Author.objects.get_or_create(name='[deleted]')[0]


class NewsArticle(models.Model):
    author = models.ForeignKey(to='Author', on_delete=models.SET(get_deleted_author))
    publication_time = models.DateTimeField(auto_now_add=True)
    last_edit_time = models.DateTimeField(auto_now=True)
    view_count = models.BigIntegerField(default=0)
    text = models.TextField()
    header = models.CharField(max_length=360)

    class Meta:
        ordering = ['-publication_time']

    def __str__(self):
        return self.header

    def get_absolute_url(self):
        return reverse('model-detail-view', args=[str(self.id)])


# CheckNone
def cnn(data):
    return '' if data is None else data


# CheckNone with number
def cnnn(data):
    return 0 if data is None else data


def user_prepare_permissions():
    content_type = ContentType.objects.get_for_model(Author)
    Permission.objects.get_or_create(codename='modify_author', name='Modify Authors', content_type=content_type)
    content_type = ContentType.objects.get_for_model(NewsArticle)
    Permission.objects.get_or_create(codename='modify_article', name='Modify Articles', content_type=content_type)


def user_add_moderator_rights(pk):
    ct = ContentType.objects.get_for_model(Author)
    perm = Permission.objects.get(codename='modify_author', content_type=ct)
    user_get_user(pk).user_permissions.add(perm)
    ct = ContentType.objects.get_for_model(NewsArticle)
    perm = Permission.objects.get(codename='modify_article', content_type=ct)
    user_get_user(pk).user_permissions.add(perm)
    return user_get_user(pk)


def user_is_moderator(username):
    return user_get_user_un(username).has_perm('news.modify_author')  # that's enough for now


def user_add_user(login, password, email='', is_admin=False):
    user = User.objects.create_user(username=login, password=password, email=email, is_staff=is_admin, is_superuser=is_admin)
    user.save()
    return user


def user_get_user(pk):
    return User.objects.filter(pk=pk).get()


def user_get_user_un(username):
    return User.objects.filter(username=username).get()


def user_delete_user(pk):
    try:
        user_get_user(pk).delete()
    finally:
        pass


def user_edit_user(user, login=None, password=None, email=None):
    save = False
    if login is not None and login != '':
        user.username = login
        save = True
    if password is not None and password != '':
        user.set_password(password)
        save = True
    if email is not None and email != '':
        user.email = email
        save = True
    if save:
        user.save()
    return user


def user_edit_user1(pk, login=None, password=None, email=None):
    return user_edit_user(user_get_user(pk), login, password, email)


def author_add_author(name, surname='', job_title=''):
    author = Author(name=name, surname=cnn(surname), job_title=cnn(job_title))
    author.save()
    return author


def author_delete_author(pk):
    try:
        author = Author.objects.filter(pk=pk).get()
        if author.name == '[deleted]':
            return
        author.delete()
    finally:
        pass


def author_find_authors(name, surname='', job_title=''):
    surname = cnn(surname)
    job_title = cnn(job_title)
    name.strip()
    surname.strip()
    job_title.strip()
    if surname == '':
        if job_title == '':
            return Author.objects.filter(name__iexact=name)
        else:
            return Author.objects.filter(name__iexact=name, job_title__iexact=job_title)
    else:
        if job_title == '':
            return Author.objects.filter(name__iexact=name, surname__iexact=surname)
        else:
            return Author.objects.filter(name__iexact=name, surname__iexact=surname, job_title__iexact=job_title)


def author_edit_author(author, name=None, surname=None, job_title=None):
    save = False
    if name is not None:
        author.name = name
        save = True
    if surname is not None:
        author.surname = surname
        save = True
    if job_title is not None:
        author.job_title = job_title
        save = True
    if save:
        author.save()
    return author


def author_edit_author1(pk, name=None, surname=None, job_title=None):
    return author_edit_author(Author.objects.filter(pk=pk).get(), name, surname, job_title)


def author_get_articles(author):
    return NewsArticle.objects.filter(author=author)


def article_add_article(author, header, text='', view_count=0):
    article = NewsArticle(author=author, header=cnn(header), text=cnn(text), view_count=cnnn(view_count))
    article.save()
    return article


def article_add_article1(author_name, author_surname, header, text='', view_count=0):
    authors = author_find_authors(cnn(author_name), cnn(author_surname))
    if len(authors) == 0:
        return article_add_article(get_deleted_author(), header, text, view_count)
    return article_add_article(authors[0], header, text, view_count)


def article_delete_article(pk):
    try:
        NewsArticle.objects.filter(pk=pk).get().delete()
    finally:
        pass


def article_edit_article(article, author_name=None, author_surname=None, header=None, text=None, view_count=None):
    save = False
    if author_name is not None or author_surname is not None:
        article.author = author_find_authors(author_name, author_surname)[0]
    if header is not None:
        article.header = header
        save = True
    if text is not None:
        article.text = text
        save = True
    if view_count is not None:
        article.view_count = view_count
        save = True
    if save:
        article.save()
    return article


def article_edit_article1(pk, author_name=None, author_surname=None, header=None, text=None, view_count=None):
    return article_edit_article(NewsArticle.objects.filter(pk=pk).get(), author_name, author_surname, header, text, view_count)
