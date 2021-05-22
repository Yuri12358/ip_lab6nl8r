from django.urls import path
from django.conf.urls import url
from . import views

# function-based views
"""urlpatterns = [
    path('', views.add_author, name='add_author'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_article/', views.add_article, name='add_article'),
    path('list_authors/', views.list_authors, name='list_authors'),
    path('list_articles/', views.list_articles, name='list_articles'),
    url(r"^edit_article/(?P<pk>\d+)/$", views.edit_article, name='edit_article'),
    url(r"^edit_author/(?P<pk>\d+)/$", views.edit_author, name='edit_author'),
    url(r"^article_details/(?P<pk>\d+)/$", views.article_details, name='article_details'),
    url(r"^author_details/(?P<pk>\d+)/$", views.author_details, name='author_details'),
]"""

# class-based views
urlpatterns = [
    path('', views.AddAuthorView.as_view(), name='add_author'),
    path('add_author/', views.AddAuthorView.as_view(), name='add_author'),
    path('add_article/', views.AddArticleView.as_view(), name='add_article'),
    path('list_authors/', views.ListAuthorsView.as_view(), name='list_authors'),
    path('list_articles/', views.ListArticlesView.as_view(), name='list_articles'),
    url(r"^edit_article/(?P<pk>\d+)/$", views.EditArticleView.as_view(), name='edit_article'),
    url(r"^edit_author/(?P<pk>\d+)/$", views.EditAuthorView.as_view(), name='edit_author'),
    url(r"^article_details/(?P<pk>\d+)/$", views.ArticleDetailsView.as_view(), name='article_details'),
    url(r"^author_details/(?P<pk>\d+)/$", views.AuthorDetailsView.as_view(), name='author_details'),
]
