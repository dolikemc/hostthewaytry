from django.views.generic import CreateView

from article.models import TextArticle, ImageArticle


# from django.utils.translation import gettext_lazy as _


class TextArticleForm(CreateView):
    model = TextArticle
    fields = '__all__'


class ImageArticleForm(CreateView):
    model = ImageArticle
    fields = '__all__'
