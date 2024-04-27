from django import forms
from .models import Report

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ReportForm(forms.Form):
    title = forms.CharField(max_length=500)
    text = forms.CharField(max_length=2000, required=True)
    location = forms.CharField(max_length=500, required=True)
    files = MultipleFileField()
    URGENCY_CHOICES = [
        (1, '1 - Not urgent'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5 - Very urgent'),
    ]
    urgency = forms.ChoiceField(choices=URGENCY_CHOICES, widget=forms.RadioSelect)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError("Please provide a title for the report.")
        return title

    def clean_location(self):
        location = self.cleaned_data.get('location')
        if not location:
            raise forms.ValidationError("Please provide a location for the report.")
        return location

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if not text:
            raise forms.ValidationError("Please provide a comment for the report.")
        return text