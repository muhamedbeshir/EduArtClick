from django import forms
from django.utils.translation import gettext_lazy as _
from v1.db.models import SchoolAccommodationPreferance




class SchoolAccommodationPreferanceForm(forms.ModelForm):

	name = forms.CharField(widget=forms.TextInput(attrs={
         'class': 'course-formset-field form-control'
     }), label="Name", label_suffix="")
	
	class Meta:
		model = SchoolAccommodationPreferance
		fields = ('name',)


