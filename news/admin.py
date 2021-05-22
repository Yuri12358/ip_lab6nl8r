from django.contrib import admin
from .models import Author, NewsArticle


class ArticleInline(admin.TabularInline):
    model = NewsArticle


class ViewCountListFilter(admin.SimpleListFilter):
    title = 'View count'
    parameter_name = 'view_cnt'

    def lookups(self, request, model_admin):
        return (
            ('100+', '100+ views'),
            ('10+', '11...100 views'),
            ('1+', '1...10 views'),
            ('0', 'Not viewed'),
        )

    def queryset(self, request, queryset):
        if self.value() == '100+':
            return queryset.filter(view_count__gt=100)
        if self.value() == '10+':
            return queryset.filter(view_count__gt=10, view_count__lte=100)
        if self.value() == '1+':
            return queryset.filter(view_count__gt=0, view_count__lte=10)
        if self.value() == '0':
            return queryset.filter(view_count__exact=0)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'job_title')
    list_filter = ('job_title',)
    inlines = [ArticleInline]


class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('header', 'author', 'publication_time', 'view_count')
    list_filter = (ViewCountListFilter,)


admin.site.register(Author, AuthorAdmin)
admin.site.register(NewsArticle, NewsArticleAdmin)
admin.site.site_header = 'Articles and authors'
