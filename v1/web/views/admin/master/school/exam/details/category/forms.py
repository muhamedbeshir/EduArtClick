from django import forms
from django.utils.translation import gettext_lazy as _
from v1.db.models import SchoolExamCategory


class SchoolExamCategoryForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg text-capitalize',
        'placeholder': 'Exam Category Name'
    }), error_messages={'required': 'School Exam Category name is required !'}, label="Exam Category Name", label_suffix="")

    class Meta:
        model = SchoolExamCategory
        fields = ['name']

    def clean_name(self):
        return f"{self.cleaned_data['name']}".title()
