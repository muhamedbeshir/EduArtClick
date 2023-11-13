from django import forms
from django.utils.translation import gettext_lazy as _
from v1.db.models import SchoolAccommodationType




class SchoolAccommodationTypeForm(forms.ModelForm):

	accommodation_type_name = forms.CharField(widget=forms.TextInput(attrs={
         'class': 'course-formset-field form-control'
     }), label="Accommodation type name", label_suffix="")
	
	class Meta:
		model = SchoolAccommodationType
		fields = ('accommodation_type_name',)


