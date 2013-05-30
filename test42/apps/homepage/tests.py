from django.test import RequestFactory, TestCase
from .models import Info
from .views import home

class InfoModelTestCase(TestCase):
    def setUp(self):
        self.info = Info.objects.create(
            first_name="Bob",
            last_name="Jones",
            birthday="1990-01-01",
            bio = "My biography",
            email = "bob@jones.com",
            jabber = "bob@jabber.org",
            skype = "bobjones",
            contacts = "Contacts"
        )

    def test_info_model(self):
        self.assertEqual(self.info.first_name, "Bob")
        self.assertEqual(self.info.last_name, "Jones")
        self.assertEqual(unicode(self.info), "Bob Jones")
        self.assertEqual(unicode(self.info.birthday), "1990-01-01")
        self.assertEqual(unicode(self.info.bio), "My biography")
        self.assertEqual(unicode(self.info.email), "bob@jones.com")
        self.assertEqual(unicode(self.info.jabber), "bob@jabber.org")
        self.assertEqual(unicode(self.info.skype), "bobjones")
        self.assertEqual(unicode(self.info.contacts), "Contacts")


class ViewTestCase(TestCase):
    def test_home_context(self):
        request = RequestFactory().get('/')
        response = home(request)
        self.assertContains(response, "Constantine", status_code=200)
        self.assertContains(response, "Fedenko", status_code=200)
        self.assertContains(response, "My bio", status_code=200)
        self.assertContains(response, "My bio", status_code=200)
        self.assertContains(response, "cfedenko@gmail.com", status_code=200)
        self.assertContains(response, "fedenko@jabber.org", status_code=200)
        self.assertContains(response, "cfedenko", status_code=200)
        self.assertContains(response, "My Contacts", status_code=200)
        Info.objects.all().delete()
        request = RequestFactory().get('/')
        response = home(request)
        self.assertNotContains(response, "Constantine", status_code=200)

