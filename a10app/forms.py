from django import forms
from .models import Report

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        print(data)
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ReportForm(forms.Form):
    title = forms.CharField(max_length=500)
    text = forms.CharField(max_length=2000, required=False)
    files = MultipleFileField()
    URGENCY_CHOICES = [
        (1, '1 - Not urgent'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5 - Very urgent'),
    ]
    urgency = forms.ChoiceField(choices=URGENCY_CHOICES, widget=forms.RadioSelect)


