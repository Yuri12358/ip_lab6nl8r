from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views import View
from news.forms import *
from news.models import *


def add_author(request):
    context = {}
    if request.method == 'POST':
        form = AddAuthorForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            job_title = form.cleaned_data['job_title']
            author_add_author(name, surname, job_title)
    else:
        form = AddAuthorForm()
    context['form'] = form
    return render(request, 'add_author.html', context=context)


def add_article(request):
    context = {}
    if request.method == 'POST':
        form = AddArticleForm(request.POST)
        if form.is_valid():
            author_name = form.cleaned_data['author_name']
            author_surname = form.cleaned_data['author_surname']
            view_count = form.cleaned_data['view_count']
            header = form.cleaned_data['header']
            text = form.cleaned_data['text']
            article_add_article1(author_name, author_surname, header, text, view_count)
    else:
        form = AddArticleForm()
    context['form'] = form
    return render(request, 'add_article.html', context=context)


def list_authors(request):
    context = {}
    if request.method == 'POST':
        if 'upd' in request.POST:
            return HttpResponseRedirect(reverse('edit_author', kwargs={'pk': request.POST['upd']}))
        elif 'del' in request.POST:
            author_delete_author(request.POST['del'])
        elif 'det' in request.POST:
            return HttpResponseRedirect(reverse('author_details', kwargs={'pk': request.POST['det']}))
    context['lines'] = Author.objects.all()
    return render(request, 'list_authors.html', context=context)


def list_articles(request):
    context = {}
    if request.method == 'POST':
        if 'upd' in request.POST:
            return HttpResponseRedirect(reverse('edit_article', kwargs={'pk': request.POST['upd']}))
        elif 'del' in request.POST:
            article_delete_article(request.POST['del'])
        elif 'det' in request.POST:
            return HttpResponseRedirect(reverse('article_details', kwargs={'pk': request.POST['det']}))
    context['lines'] = NewsArticle.objects.all()
    return render(request, 'list_articles.html', context=context)


def edit_article(request, pk):
    context = {}
    if request.method == 'POST':
        form = EditArticleForm(request.POST)
        if form.is_valid():
            author_name = form.cleaned_data['author_name']
            author_surname = form.cleaned_data['author_surname']
            view_count = form.cleaned_data['view_count']
            header = form.cleaned_data['header']
            text = form.cleaned_data['text']
            article_edit_article1(pk, author_name, author_surname, header, text, view_count)
    article = NewsArticle.objects.filter(pk=pk).get()
    form = EditArticleForm(initial={'author_name': article.author.name, 'author_surname': article.author.surname, 'view_count': article.view_count, 'header': article.header, 'text': article.text})
    context['form'] = form
    return render(request, 'edit_article.html', context=context)


def edit_author(request, pk):
    context = {}
    if request.method == 'POST':
        form = EditAuthorForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            job_title = form.cleaned_data['job_title']
            author_edit_author1(pk, name, surname, job_title)
    author = Author.objects.filter(pk=pk).get()
    form = EditAuthorForm(initial={'name': author.name, 'surname': author.surname, 'job_title': author.job_title})
    context['form'] = form
    return render(request, 'edit_author.html', context=context)


def article_details(request, pk):
    context = {}
    article = NewsArticle.objects.filter(pk=pk).get()
    article.view_count += 1
    article.save()
    lines = [
        ('ID', article.id),
        ('Author id', article.author.id),
        ('Author name', article.author.name),
        ('Author surname', article.author.surname),
        ('Author job title', article.author.job_title),
        ('Publication time', article.publication_time),
        ('Last edit time', article.last_edit_time),
        ('View count', article.view_count),
        ('Header', article.header),
        ('Text', article.text),
    ]
    context['lines'] = lines
    return render(request, 'article_details.html', context=context)


def author_details(request, pk):
    context = {}
    author = Author.objects.filter(pk=pk).get()
    articles = author_get_articles(author)
    article_headers = ''
    for article in articles:
        article_headers += article.header + ', '
    if len(article_headers) > 2:
        article_headers = article_headers[:len(article_headers) - 2]
    lines = [
        ('ID', author.id),
        ('Name', author.name),
        ('Surname', author.surname),
        ('Job title', author.job_title),
        ('Articles', article_headers),
    ]
    context['lines'] = lines
    return render(request, 'author_details.html', context=context)


class AddAuthorView(View):
    template_name = 'add_author.html'

    def get(self, request, *args, **kwargs):
        context = {'form': AddAuthorForm()}
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = AddAuthorForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            job_title = form.cleaned_data['job_title']
            author_add_author(name, surname, job_title)
        return render(request, self.template_name, context=context)


class AddArticleView(View):
    template_name = 'add_article.html'

    def get(self, request, *args, **kwargs):
        context = {'form': AddArticleForm()}
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = AddArticleForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            author_name = form.cleaned_data['author_name']
            author_surname = form.cleaned_data['author_surname']
            view_count = form.cleaned_data['view_count']
            header = form.cleaned_data['header']
            text = form.cleaned_data['text']
            article_add_article1(author_name, author_surname, header, text, view_count)
        return render(request, self.template_name, context=context)


class ListAuthorsView(View):
    template_name = 'list_authors.html'

    def common(self, request):
        return render(request, self.template_name, context={'lines': Author.objects.all()})

    def get(self, request, *args, **kwargs):
        return self.common(request)

    def post(self, request, *args, **kwargs):
        if 'upd' in request.POST:
            return HttpResponseRedirect(reverse('edit_author', kwargs={'pk': request.POST['upd']}))
        elif 'del' in request.POST:
            author_delete_author(request.POST['del'])
        elif 'det' in request.POST:
            return HttpResponseRedirect(reverse('author_details', kwargs={'pk': request.POST['det']}))
        return self.common(request)


class ListArticlesView(View):
    template_name = 'list_articles.html'

    def common(self, request):
        return render(request, self.template_name, context={'lines': NewsArticle.objects.all()})

    def get(self, request, *args, **kwargs):
        return self.common(request)

    def post(self, request, *args, **kwargs):
        if 'upd' in request.POST:
            return HttpResponseRedirect(reverse('edit_article', kwargs={'pk': request.POST['upd']}))
        elif 'del' in request.POST:
            article_delete_article(request.POST['del'])
        elif 'det' in request.POST:
            return HttpResponseRedirect(reverse('article_details', kwargs={'pk': request.POST['det']}))
        return self.common(request)


class EditArticleView(View):
    template_name = 'edit_article.html'

    def common(self, request, pk):
        article = NewsArticle.objects.filter(pk=pk).get()
        form = EditArticleForm(initial={
            'author_name': article.author.name,
            'author_surname': article.author.surname,
            'view_count': article.view_count,
            'header': article.header,
            'text': article.text
        })
        return render(request, self.template_name, context={'form': form})

    def get(self, request, *args, **kwargs):
        return self.common(request, kwargs['pk'])

    def post(self, request, *args, **kwargs):
        form = EditArticleForm(request.POST)
        if form.is_valid():
            author_name = form.cleaned_data['author_name']
            author_surname = form.cleaned_data['author_surname']
            view_count = form.cleaned_data['view_count']
            header = form.cleaned_data['header']
            text = form.cleaned_data['text']
            article_edit_article1(kwargs['pk'], author_name, author_surname, header, text, view_count)
        return self.common(request, kwargs['pk'])


class EditAuthorView(View):
    template_name = 'edit_author.html'

    def common(self, request, pk):
        author = Author.objects.filter(pk=pk).get()
        form = EditAuthorForm(initial={
            'name': author.name,
            'surname': author.surname,
            'job_title': author.job_title
        })
        return render(request, self.template_name, context={'form': form})

    def get(self, request, *args, **kwargs):
        return self.common(request, kwargs['pk'])

    def post(self, request, *args, **kwargs):
        form = EditAuthorForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            job_title = form.cleaned_data['job_title']
            author_edit_author1(kwargs['pk'], name, surname, job_title)
        return self.common(request, kwargs['pk'])


class ArticleDetailsView(View):
    template_name = 'article_details.html'

    def common(self, request, pk):
        article = NewsArticle.objects.filter(pk=pk).get()
        article.view_count += 1
        article.save()
        lines = [
            ('ID', article.id),
            ('Author id', article.author.id),
            ('Author name', article.author.name),
            ('Author surname', article.author.surname),
            ('Author job title', article.author.job_title),
            ('Publication time', article.publication_time),
            ('Last edit time', article.last_edit_time),
            ('View count', article.view_count),
            ('Header', article.header),
            ('Text', article.text),
        ]
        return render(request, self.template_name, context={'lines': lines})

    def get(self, request, *args, **kwargs):
        return self.common(request, kwargs['pk'])

    def post(self, request, *args, **kwargs):
        return self.common(request, kwargs['pk'])


class AuthorDetailsView(View):
    template_name = 'author_details.html'

    def common(self, request, pk):
        author = Author.objects.filter(pk=pk).get()
        articles = author_get_articles(author)
        article_headers = ''
        for article in articles:
            article_headers += article.header + ', '
        if len(article_headers) > 2:
            article_headers = article_headers[:len(article_headers) - 2]
        lines = [
            ('ID', author.id),
            ('Name', author.name),
            ('Surname', author.surname),
            ('Job title', author.job_title),
            ('Articles', article_headers),
        ]
        return render(request, self.template_name, context={'lines': lines})

    def get(self, request, *args, **kwargs):
        return self.common(request, kwargs['pk'])

    def post(self, request, *args, **kwargs):
        return self.common(request, kwargs['pk'])
