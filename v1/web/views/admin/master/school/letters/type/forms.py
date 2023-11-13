from django import forms
from django.utils.translation import gettext_lazy as _
from v1.db.models import SchoolLetterType

class SchoolLetterTypeForm(forms.ModelForm):

	name = forms.CharField(widget=forms.TextInput(attrs={
         'class': 'form-control form-control-lg text-capitalize',
		 'placeholder': 'School Letter Type Name'
     }), error_messages={'required': 'School Letter Type name is required !'}, label="School Letter Type Name", label_suffix="")

	class Meta:
		model = SchoolLetterType
		fields = ['name']

	def clean_name(self):
		return str(self.cleaned_data.get('name')).title()

