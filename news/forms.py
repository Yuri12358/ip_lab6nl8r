from django import forms
from django.core.exceptions import ValidationError
from django.forms import RadioSelect
from django.utils.translation import ugettext_lazy as _


class AddAuthorForm(forms.Form):
    name = forms.CharField(max_length=80, required=True)
    surname = forms.CharField(max_length=160, required=False)
    job_title = forms.CharField(max_length=160, required=False)


class AddArticleForm(forms.Form):
    author_name = forms.CharField(max_length=80, required=True)
    author_surname = forms.CharField(max_length=160, required=False)
    view_count = forms.IntegerField(required=False)
    header = forms.CharField(max_length=360, required=True)
    text = forms.CharField(required=True)

    def clean_view_count(self):
        cnt = self.cleaned_data['view_count']
        if cnt is not None and cnt < 0:
            raise ValidationError(_("View count can't be less than 0"))
        return cnt


class EditAuthorForm(AddAuthorForm):
    pass


class EditArticleForm(AddArticleForm):
    pass
