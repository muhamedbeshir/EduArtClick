from django import forms
from django.utils.translation import gettext_lazy as _
from v1.db.models import SchoolLetterType , SchoolLetter
from v1.base.configs import cRequest


class SchoolLetterForm(forms.ModelForm):

	ref_type = forms.ModelChoiceField(
		label='Letter Type',
		label_suffix="",
		queryset = SchoolLetterType.objects.all(),
		widget=forms.Select(attrs={'class':'form-select form-select-lg'})
		)
	
	is_default = forms.BooleanField(label='Is Default', label_suffix = "",
		required=False,
		widget=forms.widgets.CheckboxInput(attrs={'class': 'form-check-input'}),
                                 )
	content = forms.CharField(widget=forms.Textarea(attrs={
		'class': 'form-control form-control-lg',
		'cols': "40", 'rows': "3"
     }), error_messages={'required': 'School Letter content is required !'}, label="Letter Content", label_suffix="")

	class Meta:
		model = SchoolLetter
		fields = ['ref_type','is_default','content']

	def __init__(self, *args, **kwargs):
		super(__class__, self).__init__(*args, **kwargs)
		self.fields["ref_type"].queryset = SchoolLetterType.objects.filter(ref_school=cRequest.params.get( "school_id" )).all().order_by('name')
		

class SchoolLetterFormView(forms.ModelForm):
    
	ref_type = forms.ModelChoiceField(
		label='Letter Type',
		label_suffix="",
		queryset = SchoolLetterType.objects.all(),
		widget=forms.Select(attrs={'class':'form-select form-select-lg'})
		)
	
	is_default = forms.BooleanField(label='Is Default', label_suffix = "",
		required=False,
		widget=forms.widgets.CheckboxInput(attrs={'class': 'form-check-input'}),
                                 )
	content = forms.CharField(widget=forms.Textarea(attrs={
		'class': 'form-control form-control-lg',
		'cols': "40", 'rows': "3"
     }), error_messages={'required': 'School Letter content is required !'}, label="Letter Content", label_suffix="")

	class Meta:
		model = SchoolLetter
		fields = ['ref_type','is_default','content']
	
	def __init__(self, *args, **kwargs):
		super(__class__, self).__init__(*args, **kwargs)

		self.fields["ref_type"].disabled = True
		self.fields["is_default"].disabled = True
		self.fields["content"].disabled = True