from django import forms
from v1.base.configs import cRequest
from v1.db.school.school_payroll import SchoolPayroll
from v1.db.user.profile import TeacherUserProfile
from django.utils import timezone

class SchoolPayrollForm(forms.ModelForm):
    
    # ref_school_teacher = forms.ModelChoiceField(
	# 	label='School Service',
	# 	label_suffix="",
    #     required=False,
    #     queryset = TeacherUserProfile.objects.all(),
	# 	widget=forms.Select(attrs={
	# 		'class': 'form-select form-select-lg'}),
    # )
    
    class Meta:
        model = SchoolPayroll
        fields = ['ref_school_teacher', 'amount', 'payroll_date', 'receipt']
        widgets = {
			'amount': forms.NumberInput(attrs={'class': 'service-formset-field form-control form-control-lg', 'required':'required', 'placeholder': '0.00', 'min': 0}),
            'payroll_date': forms.DateInput(attrs={'class': 'form-control form-control-lg', 'type': 'date'})
		}


    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)

        self.fields['payroll_date'].widget.attrs.update({'min': timezone.now().date()})
        self.fields['receipt'].widget.attrs.update({'class': 'form-control form-control-lg'})
        self.fields['ref_school_teacher'].widget.attrs.update({'class': 'form-select form-select-lg'})

        self.fields["ref_school_teacher"].queryset = TeacherUserProfile.objects.filter(ref_school=cRequest.params.get( "school_id" )).all()

    # def clean_name(self):
    #     return str(self.cleaned_data['']).title()