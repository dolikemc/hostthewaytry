from django.http.response import HttpResponse
from django.shortcuts import reverse

from places.models import Place
from tests.article_tests.base import ArticleTest


class ArticleViewsTest(ArticleTest):
    def setUp(self):
        super().setUp()

    def test_add_text_article(self):
        self.set_up_traveller()
        self.assertTrue(self.client.login(**self.credentials))
        place = Place.objects.create(name='test', created_by=self.user)
        self.assertIsInstance(place, Place)
        response: HttpResponse = self.client.post(
            reverse('article:create-text', kwargs={'place_id': place.id}), data={'text': 'so ein tag'})
        print(response.content)
        self.assertRedirects(response, reverse('places:detail', kwargs={'pk': place.id}))
