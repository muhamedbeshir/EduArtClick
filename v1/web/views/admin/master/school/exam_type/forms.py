from django import forms
from django.utils.translation import gettext_lazy as _
from v1.db.models import SchoolExamType

class SchoolExamTypeForm(forms.ModelForm):

	name = forms.CharField(widget=forms.TextInput(attrs={
         'class': 'form-control form-control-lg text-capitalize',
		 'placeholder': 'Exam Type'
     }), error_messages={'required': 'School Exam Type name is required !'}, label="School Exam Type Name", label_suffix="")

	class Meta:
		model = SchoolExamType
		fields = ['name']

	def clean_name(self):
		return str(self.cleaned_data['name']).title()