from django import forms
from django.utils.translation import gettext_lazy as _
from v1.db.models import *
from v1.base.configs import cRequest
from v1.db.user.student_profile_has_service import StudentProfileHasService

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


class StudentProfileHasCourseForm(forms.ModelForm):

    ref_course = forms.ModelChoiceField(queryset=SchoolClass.objects.none(
    ), widget=forms.Select(attrs={'class': 'form-select form-select-lg'}))
    study_period = forms.ChoiceField(choices=STUDY_PERIOD, widget=forms.Select(
        attrs={'class': 'form-select form-select-lg'}))
    '''start_date = forms.CharField(widget=forms.TextInput(attrs={
         'class': 'form-select form-select-lg datetimepicker-input'
     }), label="Name", label_suffix="")'''
    class Meta:
        model = StudentProfileHasCourse
        fields = ('ref_course', 'study_period', 'start_date')

    def __init__(self, *args, **kwargs):
        self.logged_in_user = kwargs.pop("logged_in_user")
        super(StudentProfileHasCourseForm, self).__init__(*args, **kwargs)

        self.fields["ref_course"].queryset = SchoolClass.objects.filter(
            ref_school=self.logged_in_user)


class StudentProfileHasAccommodationForm(forms.ModelForm):
    ref_accommodation_room = forms.ModelChoiceField(queryset=SchoolAccommodationService.objects.none(
    ), widget=forms.Select(attrs={'class': 'form-select form-select-lg'}))

    class Meta:
        model = StudentProfileHasAccommodation
        fields = ('ref_accommodation_room', 'start_date', 'end_date')

    def __init__(self, *args, **kwargs):
        self.user_school_id = kwargs.pop("user_school_id")
        super(StudentProfileHasAccommodationForm,
              self).__init__(*args, **kwargs)

        self.fields["ref_accommodation_room"].queryset = SchoolAccommodationService.objects.filter(
            ref_school=self.user_school_id)


class StudentProfileHasServiceForm(forms.ModelForm):
    PER_WEEK = 1
    ONE_TIME = 2
    SERVICE_TYPE_CHOICES = (
        ('', 'Select'),
        (PER_WEEK, 'Per Week'),
        (ONE_TIME, 'One Time')
    )

    ref_service = forms.ModelChoiceField(queryset=SchoolService.objects.none(
    ), widget=forms.Select(attrs={'class': 'form-select form-select-lg'}))

    service_type = forms.ChoiceField(
        choices=SERVICE_TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-select form-select-lg'}))

    class Meta:
        model = StudentProfileHasService
        fields = ('ref_service', 'start_date', 'end_date')

    def __init__(self, *args, **kwargs):
        self.user_school_id = kwargs.pop("user_school_id")
        super(StudentProfileHasServiceForm,
              self).__init__(*args, **kwargs)

        self.fields["ref_service"].queryset = SchoolService.objects.filter(
            ref_school=self.user_school_id)

        if self.instance.pk:
            if self.instance.ref_service.service_type == 1:
                service_type = self.PER_WEEK
            elif self.instance.ref_service.service_type == 2:
                service_type = self.ONE_TIME
            self.fields["service_type"].initial = service_type


class UpdateSchoolStudentForm(forms.ModelForm):

    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_CHOICES = (
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female')
    )

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg text-capitalize', 'placeholder': 'First name', 'autocomplete': 'off'
    }), label="First name", label_suffix="")
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg text-capitalize', 'placeholder': 'Last name', 'autocomplete': 'off'
    }), label="First name", label_suffix="")

    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={
        'class': 'form-select form-select-lg', 'autocomplete': 'off'
    }), label="gender", label_suffix="")

    class Meta:
        model = SchoolStudentUserProfile
        exclude = ('ref_user', 'ref_school')
        fields = ('first_name', 'last_name', 'gender', 'date_of_birth', 'home_address', 'post_code',
                  'nationality', 'phone', 'religion', 'passport_number', 'passport_expiry_date', 'avtar')
