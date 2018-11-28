from django.test.utils import skipIf

from article.models import TextArticle, ImageArticle
from tests.article_tests.base import ArticleTest


class ArticleModelTest(ArticleTest):
    @skipIf(True, 'not yet implemented')
    def test_text_article(self):
        article = TextArticle.objects.create(text='hey')
        self.assertIsInstance(article, TextArticle)

    @skipIf(True, 'not yet implemented')
    def test_image_article(self):
        article = ImageArticle.objects.create(picture=self.get_file_pointer(), text='hey ho')
        self.assertIsInstance(article, ImageArticle)
