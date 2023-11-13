from django import forms
from v1.db.master.school_course import SchoolCourse

from v1.db.school.school_course_discount import SchoolCourseDiscount
from v1.base.configs import cRequest

class SchoolCourseDiscountForm(forms.ModelForm):

    # ref_course = forms.ModelChoiceField(
	# 	label='School Course',
	# 	label_suffix="",
	# 	queryset = SchoolCourse.objects.all(),
	# 	widget=forms.Select(attrs={
	# 		'class': 'form-select form-select-lg'})
    # )
    coupon_code = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control form-control-lg text-uppercase',
            'placeholder': 'Coupon Code'
        }), error_messages={'required': 'School Coupon Code is required !'}, label="Coupon Code", label_suffix="")
    
    is_active = forms.BooleanField(
        label='Is Active', 
        label_suffix = "",
		required=False,
		widget=forms.widgets.CheckboxInput(
            attrs={'class': 'form-check-input'}),
    )

    class Meta:
        model = SchoolCourseDiscount
        fields = ['coupon_code', 'discount', 'valid_from', 'valid_upto', 'is_active']

    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)

        # self.fields["ref_course"].queryset = SchoolCourse.objects.filter(ref_school=cRequest.params.get( "school_id" )).all()
        # print('Edit School Course Discount :: ', cRequest.params.get( "school_id" ), SchoolCourse.objects.filter(ref_school=cRequest.params.get( "school_id" )))

    def clean_coupon_code(self):
        return str(self.cleaned_data['coupon_code']).upper()