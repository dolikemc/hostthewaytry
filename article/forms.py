import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.transaction import atomic
from django.http.response import HttpResponseRedirect
from django.shortcuts import reverse
from django.views.generic import CreateView

from article.models import TextArticle, ImageArticle

# Get an instance of a logger
logger: logging.Logger = logging.getLogger(__name__)


# from django.utils.translation import get text_lazy as _
class AbstractArticleForm(LoginRequiredMixin, CreateView):
    login_url = '/traveller/login/'
    template_name = 'article/article_form.html'
    initial = {'rank': 1, }

    def get_success_url(self):
        return reverse('places:detail', kwargs={'pk': self.get_place_id()})

    def get_place_id(self):
        return self.kwargs['place_id']

    @atomic
    def form_valid(self, form):
        logger.debug(self.request.POST)
        place = form.save(commit=False)
        place.created_by = self.request.user
        place.save()
        return HttpResponseRedirect(self.get_success_url())


class TextArticleForm(AbstractArticleForm):
    model = TextArticle
    fields = ['text']


class ImageArticleForm(AbstractArticleForm):
    model = ImageArticle
    fields = ['text', 'picture', 'copyright']
