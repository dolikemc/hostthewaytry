from django.contrib import admin

from article.models import TextArticle, ImageArticle

# Register your models here.

admin.site.register(TextArticle)
admin.site.register(ImageArticle)
