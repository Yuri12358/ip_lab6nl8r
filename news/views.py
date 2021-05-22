from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views import View
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth import login as dj_login
from news.forms import *
from news.models import *


def check_request_auth(request):
    if not request.user.is_authenticated:
        return False, None
    return True, request.user.username


def check_moderator(request):
    ok, un = check_request_auth(request)
    if not ok:
        return False
    return user_is_moderator(un)


def fill_auth_ctx(request, context):
    ok, login = check_request_auth(request)
    context['logged_in'] = ok
    context['can_edit'] = check_moderator(request)
    if ok:
        context['username'] = login


class AddAuthorView(View):
    template_name = 'add_author.html'

    def get(self, request, *args, **kwargs):
        context = {'form': AddAuthorForm()}
        fill_auth_ctx(request, context)
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = AddAuthorForm(request.POST)
        context = {'form': form}
        fill_auth_ctx(request, context)
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
        fill_auth_ctx(request, context)
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = AddArticleForm(request.POST)
        context = {'form': form}
        fill_auth_ctx(request, context)
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
        context = {'lines': Author.objects.all()}
        fill_auth_ctx(request, context)
        return render(request, self.template_name, context=context)

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
        context = {'lines': NewsArticle.objects.all()}
        fill_auth_ctx(request, context)
        return render(request, self.template_name, context=context)

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
        context = {'form': form}
        fill_auth_ctx(request, context)
        return render(request, self.template_name, context=context)

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
        context = {'form': form}
        fill_auth_ctx(request, context)
        return render(request, self.template_name, context=context)

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
        context = {'lines': lines}
        fill_auth_ctx(request, context)
        return render(request, self.template_name, context=context)

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
        context = {'lines': lines}
        fill_auth_ctx(request, context)
        return render(request, self.template_name, context=context)

    def get(self, request, *args, **kwargs):
        return self.common(request, kwargs['pk'])

    def post(self, request, *args, **kwargs):
        return self.common(request, kwargs['pk'])


class ChangeUserDataView(View):
    template_name = 'change_user_data.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={'form': ChangeUserDataForm()})

    def post(self, request, *args, **kwargs):
        if 'apply' in request.POST:
            ok, curr_un = check_request_auth(request)
            if ok:
                user_edit_user(user_get_user_un(curr_un), request.POST['login'], request.POST['password'])
                return HttpResponseRedirect(reverse('list_authors'))
        return render(request, self.template_name, context={'form': ChangeUserDataForm()})


class LogInView(View):
    template_name = 'log_in.html'

    @staticmethod
    def to_signup():
        return HttpResponseRedirect(reverse('sign_up'))

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={'form': LogInForm()})

    def post(self, request, *args, **kwargs):
        if 'log_in' in request.POST:
            user = authenticate(username=request.POST['login'], password=request.POST['password'])
            if user is None:
                return render(request, self.template_name, context={'form': LogInForm(), 'error': 'Invalid username or password'})
            if not user.is_active:
                return render(request, self.template_name, context={'form': LogInForm(), 'error': 'Inactive user'})
            dj_login(request, user)
            return HttpResponseRedirect(reverse('list_authors'))
        elif 'sign_up' in request.POST:
            pass
        return self.to_signup()


class LogOutView(View):
    template_name = 'log_out.html'

    def common(self, request):
        context = {}
        if not request.user.is_authenticated:
            context['result'] = 'Error: Not authenticated'
        else:
            logout(request)
            context['result'] = 'Logged out successfully'
        return render(request, self.template_name, context=context)

    def get(self, request, *args, **kwargs):
        return self.common(request)

    def post(self, request, *args, **kwargs):
        return self.common(request)


class SignUpView(View):
    template_name = 'sign_up.html'

    @staticmethod
    def to_login():
        return HttpResponseRedirect(reverse('log_in'))

    def get(self, request, *args, **kwargs):
        user_prepare_permissions()
        return render(request, self.template_name, context={'form': SignUpForm()})

    def post(self, request, *args, **kwargs):
        if 'log_in' in request.POST:
            pass
        elif 'sign_up_u' in request.POST:
            user_add_user(request.POST['login'], request.POST['password'], request.POST['email'])
        elif 'sign_up_m' in request.POST:
            user = user_add_user(request.POST['login'], request.POST['password'], request.POST['email'])
            user_add_moderator_rights(user.pk)
        elif 'sign_up_a' in request.POST:
            user_add_user(request.POST['login'], request.POST['password'], request.POST['email'], True)
        return self.to_login()
