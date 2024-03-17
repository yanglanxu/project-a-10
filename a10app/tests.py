from django.test import TestCase
from django.utils.datastructures import MultiValueDict
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import Group, User

from a10app.forms import ReportForm
from a10app.templatetags.auth_extras import has_group


# Create your tests here.
class ReportFormTests(TestCase):
    def setUp(self):
        self.test_text = "Test text"
        self.test_title = "Test title"
        self.empty_form = ReportForm(data={})
        self.full_form = ReportForm(data={"title":self.test_title, "text":self.test_text})

    def test_empty_title(self):
        self.assertEqual(self.empty_form.errors["title"],["This field is required."])

    def test_non_empty_title(self):
        self.assertTrue("title" not in self.full_form.errors.keys())

    def test_empty_text(self):
        self.assertTrue("text" not in self.empty_form.errors.keys())

    def test_non_empty_text(self):
        self.assertTrue("text" not in self.full_form.errors.keys())

class UserAuthTests(TestCase):
    def setUp(self):
        self.group_name = "My Test Group"
        self.group = Group(name=self.group_name)
        self.group.save()
        self.user = User.objects.create(username="test", email="test@test.com", password="test")

    def tearDown(self):
        self.user.delete()
        self.group.delete()

    def test_user_not_group(self):
        self.assertFalse(has_group(self.user, self.group_name))

    def test_user_has_group(self):
        self.user.groups.add(self.group)
        self.user.save()
        self.assertTrue(has_group(self.user, self.group_name))
