from django import forms
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from v1.db.models import Country



class CountryForm(forms.ModelForm):

	country_name = forms.CharField(widget=forms.TextInput(attrs={
		'class': 'form-control form-control-lg text-capitalize',
		'placeholder': 'Country Name',
	}), error_messages={'required': 'Country name is required !'}, label="Country Name", label_suffix="")

	class Meta:
		model = Country
		fields = ['country_name']

	def clean_country_name(self):
		return str(self.cleaned_data['country_name']).title()