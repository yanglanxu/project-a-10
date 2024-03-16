from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import Group, User

from a10app.forms import ReportForm
from a10app.templatetags.auth_extras import has_group


# Create your tests here.
class ReportFormTests(TestCase):
    def test_empty_title(self):
        form = ReportForm(data={})

        self.assertEqual(form.errors["title"],["This field is required."])

    def test_non_empty_title(self):
        form = ReportForm(data={"title":"Test Title"})

        self.assertTrue("title" not in form.errors.keys())

    def test_empty_text(self):
        form = ReportForm(data={})

        self.assertTrue("text" not in form.errors.keys())

    def test_non_empty_text(self):
        form = ReportForm(data={"text": "Test Text"})

        self.assertTrue("text" not in form.errors.keys())

    def test_non_empty_file(self):
        testfile = SimpleUploadedFile("testfile.pdf", b"file_content")
        form = ReportForm(data={"files": testfile})
        self.assertTrue("files" not in form.errors.keys())

    def test_empty_file(self):
        form = ReportForm(data={})
        self.assertTrue("files" not in form.errors.keys())

class UserAuthTests(TestCase):
    def setUp(self):
        # create permissions group
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
