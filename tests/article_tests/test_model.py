from article.models import TextArticle, ImageArticle
from tests.article_tests.base import ArticleTest
from traveller.models import User


class ArticleModelTest(ArticleTest):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create(email='a@b.de')

    def test_text_article(self):
        article = TextArticle.objects.create(text='hey', created_by=self.user)
        self.assertIsInstance(article, TextArticle)

    def test_image_article(self):
        article = ImageArticle.objects.create(picture=self.get_file_pointer(), text='hey ho', created_by=self.user)
        self.assertIsInstance(article, ImageArticle)
