import os.path
import tempfile
from StringIO import StringIO
from django.conf import settings
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.template import Template, Context
from django.test import TestCase
from django.test.utils import override_settings
from ..models import Info, LogEntry, ActionEntry

DATA_DIR = os.path.join(os.path.normpath(os.path.dirname(__file__)), "data/")


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class InfoModelTestCase(TestCase):
    def setUp(self):
        self.info = Info.objects.create(
            first_name="Bob",
            last_name="Jones",
            birthday="1990-01-01",
            bio="My biography",
            email="bob@jones.com",
            jabber="bob@jabber.org",
            skype="bobjones",
            contacts="Contacts",
            photo=File(open(os.path.join(DATA_DIR, "Lenna.jpg"), "rb"))
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
        self.failUnless(open(self.info.photo.path), 'file not found')


class LogEntryModelTestCase(TestCase):
    def setUp(self):
        self.logentry = LogEntry.objects.create(
            method="GET",
            url="/about/",
            status=200
        )

    def test_logentry_model(self):
        self.assertEqual(self.logentry.method, "GET")
        self.assertEqual(self.logentry.url, "/about/")
        self.assertEqual(self.logentry.status, 200)


class ViewTestCase(TestCase):
    def setUp(self):
        self.auth = {"username": "admin", "password": "admin"}

    def test_home_context(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, "Constantine", status_code=200)
        self.assertContains(response, "Fedenko", status_code=200)
        self.assertContains(response, "My bio", status_code=200)
        self.assertContains(response, "1988", status_code=200)
        self.assertContains(response, "cfedenko@gmail.com", status_code=200)
        self.assertContains(response, "fedenko@jabber.org", status_code=200)
        self.assertContains(response, "cfedenko", status_code=200)
        self.assertContains(response, "My Contacts", status_code=200)
        Info.objects.all().delete()
        response = self.client.get(reverse('home'))
        self.assertNotContains(response, "Constantine", status_code=200)

    def test_log_context(self):
        for i in xrange(11):
            self.client.get(reverse('home'))

        response = self.client.get(reverse('log'))
        entry_list = response.context[-1]['entry_list']
        self.assertEqual(len(entry_list), 10)

    def test_auth(self):
        self.assertEqual(self.client.get(reverse('logout')).status_code, 302)
        self.assertEqual(self.client.get(reverse('home')).status_code, 200)
        self.assertEqual(self.client.get(reverse('log')).status_code, 200)
        self.assertEqual(self.client.get(reverse('edit')).status_code, 302)
        self.client.post(reverse('login'), self.auth)
        self.assertEqual(self.client.get(reverse('edit')).status_code, 200)
        self.assertEqual(self.client.get(reverse('logout')).status_code, 302)
        self.assertEqual(self.client.get(reverse('edit')).status_code, 302)

    def test_edit_form(self):
        self.client.post(reverse('login'), self.auth)
        upload_file = open(os.path.join(DATA_DIR, "Lenna.jpg"), "rb")
        data = dict(
            first_name="Bob",
            last_name="Jones",
            birthday="1990-01-01",
            bio="My biography",
            email="bob@jones.com",
            jabber="bob@jabber.org",
            skype="bobjones",
            contacts="Bob Contacts",
            photo=SimpleUploadedFile(upload_file.name, upload_file.read())
        )
        response = self.client.post(reverse('edit'), data)
        self.assertEqual(response.status_code, 302)
        upload_file.seek(0)
        data = dict(
            first_name="Constantine",
            last_name="Fedenko",
            birthday="1988-03-23",
            bio="My bio",
            email="cfedenko@gmail.com",
            jabber="fedenko@jabber.org",
            skype="cfedenko",
            contacts="My Contacts",
            photo=SimpleUploadedFile(upload_file.name, upload_file.read())
        )
        response = self.client.post(reverse('edit'), data,
                                    HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(response.status_code, 200)
        upload_file.seek(0)
        data = dict(
            first_name="Constantine",
            last_name="Fedenko",
            birthday="1988-03",
            bio="My bio",
            email="cfedenko@gmail.com",
            jabber="fedenko@jabber.org",
            skype="cfedenko",
            contacts="My Contacts",
            photo=SimpleUploadedFile(upload_file.name, upload_file.read())
        )
        response = self.client.post(reverse('edit'), data,
                                    HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertContains(response, "Enter a valid date.", status_code=400)
        response = self.client.get(reverse('home'))
        self.assertContains(response, "Constantine", status_code=200)
        self.assertContains(response, "Fedenko", status_code=200)
        self.assertContains(response, "1988", status_code=200)
        self.assertContains(response, "My bio", status_code=200)
        self.assertContains(response, "cfedenko@gmail.com", status_code=200)
        self.assertContains(response, "fedenko@jabber.org", status_code=200)
        self.assertContains(response, "cfedenko", status_code=200)
        self.assertContains(response, "My Contacts", status_code=200)


class MiddlewareModelTestCase(TestCase):

    def test_middleware(self):
        self.client.get(reverse('home'))
        entry = LogEntry.objects.latest()
        self.assertEqual(entry.method, "GET")
        self.assertEqual(entry.url, reverse('home'))
        self.assertEqual(entry.status, 200)


class ContextProcessorTestCase(TestCase):

    def test_context_processor(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.context[-1]['settings'], settings)


class TemplateTagsTestCase(TestCase):
    def setUp(self):
        self.info = Info.objects.create(
            first_name="Bob",
            last_name="Jones",
            birthday="1990-01-01",
            bio="My biography",
            email="bob@jones.com",
            jabber="bob@jabber.org",
            skype="bobjones",
            contacts="Contacts",
            photo=File(open(os.path.join(DATA_DIR, "Lenna.jpg"), "rb"))
        )

    def test_admin_url(self):
        out = Template(
            "{% load homepage_extras %}"
            "{% edit_link info %}"
        ).render(Context({
            'info': self.info
        }))
        self.assertEqual(out, reverse("admin:homepage_info_change",
                                      args=(self.info.pk,)))


class DjangoCommandTestCase(TestCase):

    def test_command(self):
        stdout_content = StringIO()
        stderr_content = StringIO()
        call_command("objcount", stdout=stdout_content, stderr=stderr_content)
        stdout_content.seek(0)
        stderr_content.seek(0)
        info_line = None
        for line in stdout_content:
            if Info.__name__ in line:
                info_line = line.strip()
        self.assertEqual(info_line,
                         "{0}: {1}".format(Info.__name__,
                                           Info.objects.count()))
        for line in stderr_content:
            if Info.__name__ in line:
                info_line = line.strip()
        self.assertEqual(info_line,
                         "error: {0}: {1}".format(Info.__name__,
                                                  Info.objects.count()))

class ActionsTestCase(TestCase):
    def setUp(self):
        from ..signalhandlers import connect
        connect()
        self.info = Info.objects.create(
            first_name="Bob",
            last_name="Jones",
            birthday="1990-01-01",
            bio="My biography",
            email="bob@jones.com",
            jabber="bob@jabber.org",
            skype="bobjones",
            contacts="Contacts",
            photo=File(open(os.path.join(DATA_DIR, "Lenna.jpg"), "rb"))
        )

    def test_actions(self):
        entry0 = ActionEntry.objects.latest()
        self.assertEqual(entry0.model, Info.__name__)
        self.assertEqual(entry0.action, ActionEntry.CREATE)
        self.info.first_name="Constantine"
        self.info.save()
        entry1 = ActionEntry.objects.latest()
        self.assertEqual(entry1.model, Info.__name__)
        self.assertEqual(entry1.action, ActionEntry.EDIT)
        self.info.delete()
        entry2 = ActionEntry.objects.latest()
        self.assertEqual(entry2.model, Info.__name__)
        self.assertEqual(entry2.action, ActionEntry.DELETE)
