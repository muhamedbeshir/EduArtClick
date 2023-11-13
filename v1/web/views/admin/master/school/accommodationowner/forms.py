from django import forms
from django.utils.translation import gettext_lazy as _
from v1.db.models import SchoolAccommodationOwner, SchoolAccommodationService



class SchoolAccommodationOwnerForm(forms.ModelForm):

	HOST_FAMILY = 0
	RESIDENT = 1
	HOTEL_OR_HOSTEL = 2
	ACCOMMODATION_TYPE = (
		("", '----------'),
		(HOST_FAMILY, 'Host family'),
		(RESIDENT, 'Resident'),
		(HOTEL_OR_HOSTEL, 'Hotel/Hostel'),
	)
	accommodation_type = forms.ChoiceField(choices=ACCOMMODATION_TYPE, widget=forms.Select(attrs={'class':'form-select form-select-lg'}))
	first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}), required=False)
	last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}), required=False)
	company_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}), required=False)
	address = forms.CharField(widget=forms.Textarea({'class':'form-control form-control-lg', 'rows':'3', 'cols':'5'}))
	city = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
	country = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
	postal_code = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control form-control-lg'}))
	phone = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
	capacity = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control form-control-lg', 'placeholder': ''}))
	notes = forms.CharField(widget=forms.Textarea({'class':'form-control form-control-lg', 'rows':'2', 'cols':'4'}))

	class Meta:
		model = SchoolAccommodationOwner
		fields = ('accommodation_type','first_name', 'last_name', 'company_name', 'address', 'city', 'country', 'postal_code','email', 'phone', 'capacity', 'notes')






class SchoolAccommodationServiceForm(forms.ModelForm):

	SINGLE_ROOM = 0
	DOUBLE_ROOM = 1
	
	ROOM_TYPE = (
		(SINGLE_ROOM, 'Single Room'),
		(DOUBLE_ROOM, 'Double Room')
	)

	accommodation_title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg', 'required':'True'}))
	price = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control form-control-lg', 'required':'True'}))
	#address = forms.CharField(widget=forms.Textarea({'class':'form-control form-control-lg', 'rows':'3', 'cols':'5'}))
	#city = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
	#country = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
	#postal_code = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
	code = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
	room_type = forms.ChoiceField(choices=ROOM_TYPE, widget=forms.Select(attrs={'class':'form-select form-select-lg', 'style': 'width: max-content;'}))
	#distance_from_school = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
	#latitude = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control form-control-lg'}))
	#longitude = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg'}))
	notes = forms.CharField(widget=forms.Textarea({'class':'form-control form-control-lg', 'rows':'2', 'cols':'4'}), required=False)

	class Meta:
		model = SchoolAccommodationService
		fields = ('id','accommodation_title', 'price', 'room_type', 'code','notes', 'status' )

