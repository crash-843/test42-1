from django.test import RequestFactory, TestCase
from .models import Info
from .views import home

class InfoModelTestCase(TestCase):
    def setUp(self):
        self.info = Info.objects.create(first_name="Bob",
                                        last_name="Jones")

    def test_info_model(self):
        self.assertEqual(self.info.first_name, "Bob")
        self.assertEqual(self.info.last_name, "Jones")
        self.assertEqual(unicode(self.info), "Bob Jones")


class ViewTestCase(TestCase):
    def test_home_context(self):
        request = RequestFactory().get('/')
        response = home(request)
        self.assertNotContains(response, "Bob Jones", status_code=200)
        info = Info.objects.create(first_name="Bob",
                                        last_name="Jones")
        info.save()
        request = RequestFactory().get('/')
        response = home(request)
        self.assertContains(response, "Bob Jones", status_code=200)

