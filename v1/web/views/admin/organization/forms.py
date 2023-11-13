from django import forms
from django.utils.translation import gettext_lazy as _
from v1.db.models import Organization, Organization, School, City, Country, Currency, SchoolService, SchoolCourse, SchoolCoursePrice, DynamicSchoolApplicationFormField



class OrganizationForm(forms.ModelForm):

	organization_name = forms.CharField(widget=forms.TextInput(attrs={
		'class': 'form-control form-control-lg text-capitalize',
		'placeholder': 'Organization Name'
    }), error_messages={'required': 'Organization name is required !'}, label="Organization Name", label_suffix="")
	
	web_url = forms.URLField(widget=forms.URLInput(attrs={
		'class': 'form-control form-control-lg',
		'placeholder': 'https://www.xyz.com'
    }), error_messages={'invalid': 'Organization url should be like "http://www.xyz.com" !'}, label="Organization Url", label_suffix="", required=False)

	organization_logo = forms.ImageField(label="Logo", label_suffix="", required=True)



	class Meta:
		model = Organization
		fields = ['organization_name', 'web_url', 'organization_logo']

	def clean_organization_name(self):
		return str(self.cleaned_data['organization_name']).title()




class SchoolOrganizationForm(forms.ModelForm):

	school_name = forms.CharField(widget=forms.TextInput(attrs={
         'class': 'form-control'
     }), error_messages={'required': 'School name is required !'}, label="School Name", label_suffix="")

	ref_country = forms.ModelChoiceField(
		label='Country',
		label_suffix="",
		queryset = Country.objects.all(),
		widget=forms.Select(attrs={'class':'form-control'})
		)

	ref_city = forms.ModelChoiceField(queryset = City.objects.all(),  widget=forms.Select(attrs={'class':'form-control'}))

	email = forms.CharField(widget=forms.TextInput(attrs={
         'class': 'form-control'
     }), label="Email", label_suffix="")

	ref_currency = forms.ModelChoiceField(queryset = Currency.objects.all(),  widget=forms.Select(attrs={'class':'form-control'}), required=False)

	

	class Meta:
		model = School
		fields = ['school_name', 'email', 'ref_country', 'ref_city', 'ref_currency']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['ref_city'].queryset = City.objects.none()

		if 'ref_country' in self.data:
			try:
				country_id = int(self.data.get('ref_country'))
				self.fields['ref_city'].queryset = City.objects.filter(ref_country=country_id).order_by('city_name')
			except (ValueError, TypeError):
				pass
		elif self.instance.pk:
			print(self.instance.pk)
			self.fields['ref_city'].queryset = self.instance.ref_city.ref_country.country_info.order_by('city_name')

