from django.test import RequestFactory, TestCase
from django.test.client import Client
from .models import Info, LogEntry
from .views import Home


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
        self.info.save()

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


class LogEntryModelTestCase(TestCase):
    def setUp(self):
        self.logentry = LogEntry.objects.create(
            method = "GET",
            url = "/about/",
            status = 200
        )
        self.logentry.save()

    def test_logentry_model(self):
        self.assertEqual(self.logentry.method, "GET")
        self.assertEqual(self.logentry.url, "/about/")
        self.assertEqual(self.logentry.status, 200)



class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_context(self):
        request = RequestFactory().get('/')
        home = Home.as_view()
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

    def test_log_context(self):
        for i in xrange(11):
            self.client.get('/')

        response = self.client.get('/log/')
        entry_list = response.context['entry_list']
        self.assertEqual(len(entry_list), 10)


class MiddlewareModelTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_info_model(self):
        response = self.client.get('/')
        entry = LogEntry.objects.latest()
        self.assertEqual(entry.method, "GET")
        self.assertEqual(entry.url, "/")
        self.assertEqual(entry.status, 200)

