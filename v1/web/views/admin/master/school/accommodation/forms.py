from django import forms
from django.utils.translation import gettext_lazy as _
from v1.db.models import SchoolAccommodationType, SchoolAccommodationService



class SchoolAccommodationServiceForm(forms.ModelForm):
	SINGLE_ROOM = 0
	DOUBLE_ROOM = 1
	
	ROOM_TYPE = (
		(SINGLE_ROOM, 'Single Room'),
		(DOUBLE_ROOM, 'Double Room')
	)

	accommodation_title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg text-capitalize', 'placeholder': 'Room Title', 'required':'True'}))
	price = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control form-control-lg', 'required':'True', 'placeholder': '0.00'}))
	#address = forms.CharField(widget=forms.Textarea({'class':'form-control', 'rows':'3', 'cols':'5'}))
	#city = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	#country = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	#postal_code = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	code = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg', 'placeholder': 'Room Number'}))
	room_type = forms.ChoiceField(choices=ROOM_TYPE, widget=forms.Select(attrs={'class':'form-select form-select-lg'}))
	#distance_from_school = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	#latitude = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
	#longitude = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	notes = forms.CharField(widget=forms.Textarea({'class':'form-control form-control-lg text-capitalize', 'rows':'2', 'cols':'4', 'placeholder': 'Note'}))

	class Meta:
		model = SchoolAccommodationService
		fields = ('accommodation_title', 'price', 'room_type', 'code','notes', 'status' )