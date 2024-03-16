from django.test import TestCase
from a10app.forms import ReportForm
from a10app.models import User

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
