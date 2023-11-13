from django import forms
from django.utils.translation import gettext_lazy as _
from v1.db.models import *
from datetime import date

from v1.db.school.school_sponsor import SchoolSponsor

STUDY_PERIOD = (
    ("", '---------'),
    ("1", '1 Week'),
    ("2", '2 Weeks'),
    ("3", '3 Weeks'),
    ("4", '4 Weeks'),
    ("5", '5 Weeks'),
    ("6", '6 Weeks'),
    ("7", '7 Weeks'),
    ("8", '8 Weeks'),
    ("9", '9 Weeks'),
    ("10", '10 Weeks'),
    ("11", '11 Weeks'),
    ("12", '12 Weeks'),
    ("13", '13 Weeks'),
    ("14", '14 Weeks'),
    ("15", '15 Weeks'),
    ("16", '16 Weeks'),
    ("17", '17 Weeks'),
    ("18", '18 Weeks'),
    ("19", '19 Weeks'),
    ("20", '20 Weeks'),
    ("21", '21 Weeks'),
    ("22", '22 Weeks'),
    ("23", '23 Weeks'),
    ("24", '24 Weeks'),
    ("25", '25 Weeks'),
    ("26", '26 Weeks'),
    ("27", '27 Weeks'),
    ("28", '28 Weeks'),
    ("29", '29 Weeks'),
    ("30", '30 Weeks'),
    ("31", '31 Weeks'),
    ("32", '32 Weeks'),
    ("33", '33 Weeks'),
    ("34", '34 Weeks'),
    ("35", '35 Weeks'),
    ("36", '36 Weeks'),
    ("37", '37 Weeks'),
    ("38", '38 Weeks'),
    ("39", '39 Weeks'),
    ("40", '40 Weeks'),
    ("41", '41 Weeks'),
    ("42", '42 Weeks'),
    ("43", '43 Weeks'),
    ("44", '44 Weeks'),
    ("45", '45 Weeks'),
    ("46", '46 Weeks'),
    ("47", '47 Weeks'),
    ("48", '48 Weeks'),
    ("49", '49 Weeks'),
    ("50", '50 Weeks'),
    ("51", '51 Weeks'),
    ("52", '52 Weeks')
)


class CalculateForm(forms.Form):

    s_country = forms.ModelChoiceField(
        label='Selected Country',
        queryset=Country.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select form-select-lg'}),
    )
    s_city = forms.ModelChoiceField(
        label='Selected City',
        queryset=City.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select form-select-lg'}),
    )
    s_school = forms.ModelChoiceField(
        label='Selected School',
        queryset=School.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select form-select-lg'})
    )
    s_course = forms.ModelChoiceField(
        label='Selected Course',
        queryset=SchoolCourse.objects.all(),
        widget=forms.Select(attrs={
                            'class': 'form-select form-select-lg ajx_call', 'select-group-first': 'first'})
    )

    s_accommodation = forms.ModelChoiceField(
        queryset=SchoolAccommodationService.objects.all(),
        widget=forms.Select,
        required=False
    )
    s_service = forms.ModelMultipleChoiceField(
        queryset=SchoolService.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    s_price = forms.ModelMultipleChoiceField(
        # or .filter(…) if you want only some articles to show up
        queryset=SchoolCoursePrice.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'price_option'}),
    )

    study_period = forms.ChoiceField(choices=STUDY_PERIOD, widget=forms.Select(
        attrs={'class': 'form-select form-select-lg ajx_call', 'select-group-secound': 'secound'}))

    s_start_date = forms.CharField()

    # s_level = forms.ModelChoiceField(
    # 	label='Select Level',
    # 	queryset = SchoolCourseLevel.objects.all(),
    # 	widget =forms.Select(attrs={'class':'form-select form-select-lg'})
    # )
    ref_ap_coupon = forms.ModelChoiceField(
        label='Select Coupon',
        queryset=SchoolCourseDiscount.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-select form-select-lg'}),
        required=False,
    )
    ref_course_type = forms.ModelChoiceField(
        label='Select Course Type',
        queryset=SchoolCourseType.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select form-select-lg'}),
        required=False,
    )

    course_class = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control d-none'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['s_city'].queryset = City.objects.none()
        self.fields['s_school'].queryset = School.objects.none()
        self.fields['s_course'].queryset = SchoolCourse.objects.none()
        # self.fields['s_level'].queryset = SchoolCourseLevel.objects.none()
        # self.fields['ref_course_type'].queryset = SchoolCourseType.objects.none()
        self.fields['ref_ap_coupon'].queryset = SchoolCourseDiscount.objects.none()

        if 's_country' in self.data:
            try:
                country_id = int(self.data.get('s_country'))
                self.fields['s_city'].queryset = City.objects.filter(
                    ref_country=country_id).order_by('city_name')
            except (ValueError, TypeError):
                pass

        if 's_city' in self.data:
            try:
                city_id = int(self.data.get('s_city'))
                self.fields['s_school'].queryset = School.objects.filter(
                    ref_city=city_id).order_by('school_name')
            except (ValueError, TypeError):
                pass

        if 's_school' in self.data:
            try:
                school_id = int(self.data.get('s_school'))
                self.fields['s_course'].queryset = SchoolCourse.objects.filter(
                    ref_school=school_id).order_by('title')
            except (ValueError, TypeError):
                pass

        if 's_school' in self.data:
            try:
                school_id = int(self.data.get('s_school'))
                course_id = int(self.data.get('s_course'))
                # self.fields['s_level'].queryset = SchoolCourseLevel.objects.filter(ref_school=school_id).order_by('name')
                self.fields['ref_ap_coupon'].queryset = SchoolCourseDiscount.objects.filter(
                    ref_school=school_id, ref_course=course_id, is_active=True)
            except (ValueError, TypeError):
                pass


class ApplicationForm(forms.ModelForm):

    post_code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg'
    }), label="Post code", label_suffix="", required=False)
    ap_phone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg'
    }), label="Mobile", label_suffix="", required=False)
    first_language = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg'
    }), label="First Language", label_suffix="", required=False)
    ap_religion = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg'
    }), label="Religion", label_suffix="", required=False)
    created_by = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg'
    }), label="created_by", label_suffix="", required=False)

    ref_ap_nationality = forms.ModelChoiceField(queryset=Nationality.objects.all(
    ),  widget=forms.Select(attrs={'class': 'form-select form-select-lg'}))

    ref_sponsor = forms.ModelChoiceField(queryset=SchoolSponsor.objects.all(
    ),  widget=forms.Select(attrs={'class': 'form-select form-select-lg'}), required=False)

    ap_passport_number = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg'
    }), label="Passport Number", label_suffix="", required=False)

    ap_passport_expiry_date = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'form-control form-control-lg',
        'min': date.today().strftime('%Y-%m-%d'),
    }), label="Passport Expire Date", label_suffix="", required=False)

    document_file = forms.FileField(widget=forms.FileInput(attrs={
        'class': 'form-control form-control-lg',
        'accept': '.pdf',
    }), label="Document File", label_suffix="", required=True)

    sponsor_document_file = forms.FileField(widget=forms.FileInput(attrs={
        'class': 'form-control form-control-lg',
        'accept': '.pdf',
    }), label="Document File", label_suffix="", required=False)

    ap_date_of_birth = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'form-control form-control-lg',
        'max': date.today().strftime('%Y-%m-%d'),
    }), label="Date Of Birth", label_suffix="", required=True)

    class Meta:
        model = Application
        fields = (
            'ap_country',
            'ap_city',
            'ap_school',
            'ap_school_email',
            'ap_course_name',
            'ap_course_class',
            'ap_study_period',
            'ap_start_date',
            'ap_end_date',
            'ap_currency',
            'ap_course_price_total',
            # 'ref_ap_coupon',
            'ap_course_discount',
            'ap_sub_total',
            'ap_grand_total',
            'ap_first_name',
            'ap_last_name',
            'ap_gender',
            'ap_date_of_birth',
            'home_address',
            'post_code',
            'ref_ap_nationality',
            'ap_email',
            'ap_phone',
            'first_language',
            'ap_religion',
            'ap_passport_number',
            'ap_passport_expiry_date',
            'ap_json_data',
            'html_invoice',
            'ap_service_json_data',
            'document_file',
            'notes',
            'ap_level',
            'ref_sponsor',
            'sponsor_document_file'
        )


class ServiceForm(forms.Form):
    s_ser = forms.CharField(widget=forms.TextInput())


class ApplicationFormLink(forms.Form):
    # PENDDING = 0
    ACCEPTED = 1
    RENEW = 2
    APPLICATION_STATUS = (
        (ACCEPTED, 'Accepted'),
        (RENEW, 'Rejected'),
    )
    ap_status = forms.MultipleChoiceField(choices=APPLICATION_STATUS,
                                          widget=forms.CheckboxSelectMultiple(attrs={}))
    feeback = forms.CharField(widget=forms.Textarea())
    ap_approved_file = forms.FileField()


class ApplicationAprovelForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('ap_approved_file', )


class ApplicationRejectForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('ap_reject_note', )
