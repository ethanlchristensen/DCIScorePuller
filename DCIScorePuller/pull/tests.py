from django.test import TestCase
from pull.models import Corp


# Create your tests here.
class CorpTestCase(TestCase):
    def setUp(self):
        Corp.objects.create(key=69, name="ATTT Corp")

    def test_corp_name(self):
        test_corp = Corp.objects.get(key=69)
        self.assertEquals(test_corp.name, "ATTT Corp")
