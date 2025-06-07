from django import forms

from apps.courses.models import Course


class ImportCourseDataForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ("json_file",)


class ImportProverbDataForm(forms.Form):
    class Meta:
        fields = ("csv_file",)

    proverbs_json_file = forms.FileField(label="Sprichwörter-Liste", required=True)
