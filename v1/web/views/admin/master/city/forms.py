from django import forms
from django.utils.translation import gettext_lazy as _
from v1.db.models import City, Country

class CityForm(forms.ModelForm):

	ref_country = forms.ModelChoiceField(queryset = Country.objects.all(),  widget=forms.Select(attrs={
		'class':'form-select form-select-lg',
		})
	)

	city_name = forms.CharField(widget=forms.TextInput(attrs={
		'class': 'form-control form-control-lg text-capitalize',
		'placeholder': 'City Name',
     }), error_messages={'required': 'City name is required !'}, label="City Name", label_suffix="")

	class Meta:
		model = City
		fields = ['ref_country','city_name']

	def clean_city_name(self):
		return str(self.cleaned_data['city_name']).title()
