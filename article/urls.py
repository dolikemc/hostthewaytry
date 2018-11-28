from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from article.forms import ImageArticleForm, TextArticleForm

app_name = 'article'
urlpatterns = \
    [
        path('add/image/', ImageArticleForm.as_view(), name='create-image'),
        path('add/text/<int:place_id>/', TextArticleForm.as_view(), name='create-text'),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
