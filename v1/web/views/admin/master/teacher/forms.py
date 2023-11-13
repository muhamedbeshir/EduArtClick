from django import forms
from django.contrib.auth.models import User
from v1.db.models import TeacherUserProfile



class UpdateSchoolTeacherForm(forms.ModelForm):

	GENDER_MALE = 0
	GENDER_FEMALE = 1
	GENDER_CHOICES = (
		(GENDER_MALE, 'Male'),
		(GENDER_FEMALE, 'Female')
	)
	first_name = forms.CharField(widget=forms.TextInput(attrs={
         'class': 'form-control form-control-lg text-capitalize', 'placeholder': 'First name', 'autocomplete':'off'
     }), label="First name", label_suffix="")
	last_name = forms.CharField(widget=forms.TextInput(attrs={
         'class': 'form-control form-control-lg text-capitalize', 'placeholder': 'Last name', 'autocomplete':'off'
     }), label="Last name", label_suffix="")

	gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={
         'class': 'form-select form-select-lg', 'autocomplete':'off'
     }), label="gender", label_suffix="")

	date_of_birth = forms.CharField(widget=forms.DateInput(attrs={
         'class': 'form-control form-control-lg', 'placeholder': '', 'autocomplete':'off'
     }), label="Date of Birth", label_suffix="")

	lang_one = forms.CharField(widget=forms.TextInput(attrs={
         'class': 'form-control form-control-lg text-capitalize', 'placeholder': 'Language 1', 'autocomplete':'off'
     }), label="Language 1", label_suffix="")
	lang_two = forms.CharField(widget=forms.TextInput(attrs={
         'class': 'form-control form-control-lg text-capitalize', 'placeholder': 'Language 2', 'autocomplete':'off'
     }), label="Language 2", label_suffix="", required=False)
	lang_three = forms.CharField(widget=forms.TextInput(attrs={
         'class': 'form-control form-control-lg text-capitalize', 'placeholder': 'Language 3', 'autocomplete':'off'
     }), label="Language 3", label_suffix="", required=False)


	class Meta:
		model = TeacherUserProfile
		exclude = ('ref_user','ref_school')
		fields = ('first_name', 'last_name', 'gender', 'date_of_birth','lang_one', 'lang_two','lang_three', 'avtar')

	def clean_first_name(self):
		return str(self.cleaned_data['first_name']).title()

	def clean_last_name(self):
		return str(self.cleaned_data['last_name']).title()

	def clean_lang_one(self):
		return str(self.cleaned_data['lang_one']).title()

	def clean_lang_two(self):
		return str(self.cleaned_data['lang_two']).title()

	def clean_lang_three(self):
		return str(self.cleaned_data['lang_three']).title()

