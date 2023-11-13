from django import forms
from v1.base.configs import cRequest
from v1.db.master.school_course import SchoolCourse
from v1.db.master.school_service import SchoolService
from v1.db.school.school_expense import SchoolExpense
from v1.db.user.profile import TeacherUserProfile
from django.utils import timezone

class SchoolExpensesForm(forms.ModelForm):
    EXPENSE_INTERNAL = 'Internal'
    EXPENSE_EXTERNAL = 'External'
    EXPENSES_CHOICES = (
        (EXPENSE_INTERNAL, EXPENSE_INTERNAL),
        (EXPENSE_EXTERNAL, EXPENSE_EXTERNAL),
    )

    expense_type = forms.ChoiceField(
		label='Expense Type',
		label_suffix="",
        choices = EXPENSES_CHOICES,
		widget=forms.Select(attrs={
			'class': 'form-select form-select-lg'})
    )

    INTERNAL_EXPENSES_ACCOMMODATION = 'Select'
    INTERNAL_EXPENSES_COURSE = 'Course'
    INTERNAL_EXPENSES_SERVICE = 'Service'
    # INTERNAL_EXPENSES_TEACHER = 'Teacher'
    INTERNAL_EXPENSES_OTHER = 'Other'

    INTERNAL_EXPENSES_CHOICES = (
        (INTERNAL_EXPENSES_ACCOMMODATION, INTERNAL_EXPENSES_ACCOMMODATION),
        (INTERNAL_EXPENSES_COURSE, INTERNAL_EXPENSES_COURSE),
        (INTERNAL_EXPENSES_SERVICE, INTERNAL_EXPENSES_SERVICE),
        # (INTERNAL_EXPENSES_TEACHER, INTERNAL_EXPENSES_TEACHER),
        (INTERNAL_EXPENSES_OTHER, INTERNAL_EXPENSES_OTHER),
    )

    internal_expense_type = forms.ChoiceField(
		label='Internal Expense Type',
		label_suffix="",
        choices = INTERNAL_EXPENSES_CHOICES,
		widget=forms.Select(attrs={
			'class': 'form-select form-select-lg'})
    )

    ref_school_course = forms.ModelChoiceField(
		label='School Course',
		label_suffix="",
        required=False,
        queryset = SchoolCourse.objects.all(),
		widget=forms.Select(attrs={
			'class': 'form-select form-select-lg'}),
    )

    ref_school_service = forms.ModelChoiceField(
		label='School Service',
		label_suffix="",
        required=False,
        queryset = SchoolService.objects.all(),
		widget=forms.Select(attrs={
			'class': 'form-select form-select-lg'}),
    )

    # ref_school_teacher = forms.ModelChoiceField(
	# 	label='School Service',
	# 	label_suffix="",
    #     required=False,
    #     queryset = TeacherUserProfile.objects.all(),
	# 	widget=forms.Select(attrs={
	# 		'class': 'form-select form-select-lg'}),
    # )
    
    class Meta:
        model = SchoolExpense
        fields = ['expense_type', 'internal_expense_type', 'name', 'amount', 'ref_school_course', 'ref_school_service', 'expense_date', 'receipt']
        widgets = {
			'name': forms.TextInput(attrs={'class': 'service-formset-field form-control form-control-lg text-capitalize', 'required':'required', 'placeholder': 'Expenses Name'}),
			'amount': forms.NumberInput(attrs={'class': 'service-formset-field form-control form-control-lg', 'required':'required', 'placeholder': '0.00'}),
            'expense_date': forms.DateInput(attrs={'class': 'form-control form-control-lg', 'type': 'date'})
		}


    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)

        self.fields['expense_date'].widget.attrs.update({'min': timezone.now().date()})
        self.fields['receipt'].widget.attrs.update({'class': 'form-control form-control-lg'})

        self.fields["ref_school_course"].queryset = SchoolCourse.objects.filter(ref_school=cRequest.params.get( "school_id" )).all()
        self.fields["ref_school_service"].queryset = SchoolService.objects.filter(ref_school=cRequest.params.get( "school_id" )).all()
        # self.fields["ref_school_teacher"].queryset = TeacherUserProfile.objects.filter(ref_school=cRequest.params.get( "school_id" )).all()

    def clean_name(self):
        return str(self.cleaned_data['name']).title()