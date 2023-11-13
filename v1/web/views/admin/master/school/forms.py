from django import forms
from django.utils.translation import gettext_lazy as _
from v1.db.models import Organization,  School, City, Country, Currency, SchoolAccommodationService, SchoolService, SchoolCourse, SchoolCoursePrice, DynamicSchoolApplicationFormField, SchoolSchedule, SchoolRoom, SchoolCourseLevel, SchoolCourseType, WeekDayList


class SchoolForm(forms.ModelForm):

    ref_organization = forms.ModelChoiceField(
        label='Organization',
        label_suffix="",
        queryset=Organization.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select form-select-lg'})
    )

    school_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'School Name',
    }), error_messages={'required': 'School name is required !'}, label="School Name", label_suffix="")

    ref_country = forms.ModelChoiceField(
        label='Country',
        label_suffix="",
        queryset=Country.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select form-select-lg'})
    )

    ref_city = forms.ModelChoiceField(queryset=City.objects.all(
    ),  widget=forms.Select(attrs={'class': 'form-select form-select-lg'}))

    email = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg',
        'placeholder': 'Enter Email',
    }), label="Email", label_suffix="")

    ref_currency = forms.ModelChoiceField(queryset=Currency.objects.all(
    ),  widget=forms.Select(attrs={'class': 'form-select form-select-lg'}), required=True)

    # ref_organization = forms.ModelChoiceField(queryset = Organization.objects.all(),  widget=forms.Select(attrs={'class':'form-control'}), label="Organization")

    class Meta:
        model = School
        fields = ['ref_organization', 'school_name', 'email',
                  'ref_country', 'ref_city', 'ref_currency', 'postal_code', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['postal_code'].widget.attrs.update(
            {'class': 'form-control form-control-lg', 'max': 6})
        self.fields['address'].widget.attrs.update(
            {'class': 'form-control form-control-lg', 'rows': 3, })

        self.fields['ref_city'].queryset = City.objects.none()

        if 'ref_country' in self.data:
            try:
                country_id = int(self.data.get('ref_country'))
                self.fields['ref_city'].queryset = City.objects.filter(
                    ref_country=country_id).order_by('city_name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            print(self.instance.pk)
            self.fields['ref_city'].queryset = self.instance.ref_city.ref_country.country_info.order_by(
                'city_name')

    def clean_school_name(self):
        return str(self.cleaned_data.get('school_name')).title()


class SchoolServiceForm(forms.ModelForm):
    PER_WEEK = 1
    ONE_TIME = 2
    SERVICE_TYPE_CHOICES = (
        (PER_WEEK, 'Per Week'),
        (ONE_TIME, 'One Time')
    )
    service_type = forms.ChoiceField(choices=SERVICE_TYPE_CHOICES, widget=forms.Select(
        attrs={'class': 'service-formset-field form-select form-select-lg', 'required': 'required', 'style': 'width: auto;'}))

    class Meta:
        model = SchoolService
        fields = ('service_type', 'service_name', 'price')

        widgets = {
            'service_name': forms.TextInput(attrs={'class': 'service-formset-field form-control form-control-lg text-capitalize', 'required': 'required', 'placeholder': 'Service name'}),
            'price': forms.NumberInput(attrs={'class': 'service-formset-field form-control form-control-lg', 'required': 'required', 'placeholder': '0.00'}),
        }

    def clean_service_name(self):
        return str(self.cleaned_data.get('service_name')).title()


class SchoolAccommodationServiceForm(forms.ModelForm):

    accommodation_title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'formset-field form-control', 'required': 'True'}))
    price = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'formset-field form-control', 'required': 'True'}))

    class Meta:
        model = SchoolAccommodationService
        fields = ('accommodation_title', 'price')


class SchoolCourseForm(forms.ModelForm):

    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'course-formset-field form-control'
    }), label="Course Name", label_suffix="")

    class Meta:
        model = SchoolCourse
        fields = ('title',)

    def clean_name(self):
        return str(self.cleaned_data.get('name')).title()


class SchoolClassForm(forms.ModelForm):

    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'course-formset-field form-control'
    }), label="Course Name", label_suffix="")
    ref_day = forms.ModelMultipleChoiceField(queryset=WeekDayList.objects.all(), widget=forms.SelectMultiple(
        attrs={'class': 'select2bs4', 'multiple': 'multiple', 'data-placeholder': 'Select a day"'}),)

    class Meta:
        model = SchoolCourse
        fields = ('title', 'ref_day',)

    def clean_name(self):
        return str(self.cleaned_data.get('name')).title()


class SchoolCoursePriceForm(forms.ModelForm):
    class Meta:
        model = SchoolCoursePrice
        fields = ('min_weak', 'max_weak', 'price')
        widgets = {
            'min_weak': forms.TextInput(attrs={'class': 'formset-field form-control form-control-lg min-weak', 'type': 'number', 'min': 0}),
            'max_weak': forms.TextInput(attrs={'class': 'formset-field form-control form-control-lg max-weak', 'type': 'number', 'min': 0}),
            'price': forms.TextInput(attrs={'class': 'formset-field form-control form-control-lg'})
        }


class DynamicSchoolApplicationFormFieldForm(forms.ModelForm):

    # type = forms.CharField(widget=forms.TextInput(attrs={'class':'formset-field form-control'}))
    class Meta:
        model = DynamicSchoolApplicationFormField
        fields = ('label', 'name', 'attributes')
        widgets = {
            'label': forms.TextInput(attrs={'class': 'formset-field form-control'}),
            'name': forms.TextInput(attrs={'class': 'formset-field form-control'}),
            'attributes': forms.TextInput(attrs={'class': 'formset-field form-control'})
        }


class SchoolScheduleForm(forms.ModelForm):

    class Meta:
        model = SchoolSchedule
        fields = ('start_time', 'end_time')


class SchoolRoomForm(forms.ModelForm):

    class Meta:
        model = SchoolRoom
        fields = ('name', 'capacity', 'minimum')

    def clean_name(self):
        return str(self.cleaned_data.get('name')).title()


class SchoolCourseLevelForm(forms.ModelForm):
    class Meta:
        model = SchoolCourseLevel
        fields = ('name',)

    def clean_name(self):
        return str(self.cleaned_data.get('name')).title()


class SchoolCourseTypeForm(forms.ModelForm):

    class Meta:
        model = SchoolCourseType
        fields = ('name',)

    def clean_name(self):
        return str(self.cleaned_data.get('name')).title()
