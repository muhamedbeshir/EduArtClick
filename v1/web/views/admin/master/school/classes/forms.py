from datetime import date, timedelta
from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from v1.db.models import SchoolRoom, SchoolCourse, SchoolCoursePrice, SchoolCourseLevel, SchoolCourseType, WeekDayList
from django.contrib.auth.models import User, Group

from v1.db.models import TeacherUserProfile
from v1.web.views.admin.master import teacher
from v1.db.master.school_class import *

# Current Date
current_day = date.today()


class SchoolClassForm(forms.ModelForm):

    DAYS_CHOICES = (
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    )

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg text-capitalize',
                'placeholder': 'eg: XYZ Course - 20 Hours, Regular'
            }
        )
    )

    minimum = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Minimum Student',
                'min': 0,
            }
        ),
        label="Minimum Student", label_suffix="",
    )

    maximum = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Maximum Student',
                'min': 0,
            }
        ),
        label="Maximum Student", label_suffix="",
    )

    # ref_course = forms.ModelChoiceField(
    #     widget=forms.Select(
    #         attrs={
    #             'class': 'form-select form-select-lg',
    #         }
    #     ),
    #     label="Select Course", label_suffix="",
    #     queryset=SchoolCourse.objects.none(),
    # )

    ref_level = forms.ModelChoiceField(
        widget=forms.Select(
            attrs={
                'class': 'form-select form-select-lg',
            }
        ),
        label="Select Level", label_suffix="",
        queryset=SchoolCourseLevel.objects.none(),
    )

    ref_teacher_name = forms.ModelChoiceField(
        widget=forms.Select(
            attrs={
                'class': 'form-select form-select-lg',
            }
        ),
        label="Select Teacher", label_suffix="",
        queryset=User.objects.all(),
    )

    ref_schedule = forms.ModelChoiceField(
        widget=forms.Select(
            attrs={
                'class': 'form-select form-select-lg',
            }
        ),
        label="Select Schedule", label_suffix="",
        queryset=SchoolSchedule.objects.none(),
    )

    ref_room = forms.ModelChoiceField(
        widget=forms.Select(
            attrs={
                'class': 'form-select form-select-lg',
            }
        ),
        label="Select Room", label_suffix="",
        queryset=SchoolRoom.objects.none(),
    )

    ref_type_of_course = forms.ModelChoiceField(
        widget=forms.Select(
            attrs={
                'class': 'form-select form-select-lg',
            }
        ),
        label="Select Room", label_suffix="",
        queryset=SchoolCourseType.objects.none(),
    )

    summar_start = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control form-control-lg datetimepicker-input',
                'placeholder': "YYYY-MM-DD",
                'type': 'date',
                'min': current_day,
            }
        ),
        label="Course Start Date", label_suffix="",
    )

    summar_end = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control form-control-lg datetimepicker-input',
                'placeholder': "YYYY-MM-DD",
                'type': 'date',
                'min': summar_start,
            }
        ),
        label="Course Start Date", label_suffix="",
    )

    note = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'course-formset-field form-control form-control-lg text-capitalize', 'rows': 4, 'cols': 10,
        'placeholder': 'eg: Course Note'
    }), label="Note", label_suffix="", required=False)

    document = forms.FileField(widget=forms.FileInput(attrs={
        'class': 'form-control form-control-lg',
        'accept': 'application/pdf',
    }), label="Document", label_suffix="", required=False)

    start_day = forms.ChoiceField(
        label="Class Start Day", choices=DAYS_CHOICES, widget=forms.Select(attrs={'class': 'form-select form-select-lg'}))

    # ref_day = forms.ModelMultipleChoiceField(queryset = WeekDayList.objects.all(), widget=forms.CheckboxSelectMultiple(),)

    class Meta:
        model = SchoolClass
        fields = ('title', 'maximum', 'minimum', 'ref_teacher_name', 'ref_schedule',
                  'ref_level', 'ref_type_of_course', 'summar_start', 'summar_end', 'start_day', 'ref_room', 'note', 'document')

    def __init__(self, *args, **kwargs):
        print('=>'*10, kwargs)
        if kwargs.get("logged_in_user"):
            self.logged_in_user = kwargs.pop("logged_in_user")
        else:
            self.logged_in_user = kwargs.get("logged_in_user")

        user_type = kwargs.get("user_type")
        print("=======================forms==================")
        print(self.logged_in_user)
        super(SchoolClassForm, self).__init__(*args, **kwargs)

        # self.fields['start_day'].widget.attrs.update({'class': 'form-control'})

        if user_type == None:
            self.fields["ref_level"].queryset = SchoolCourseLevel.objects.filter(
                ref_school=self.logged_in_user).order_by('name')
            # self.fields["ref_teacher_name"].queryset = TeacherUserProfile.objects.filter(
            #     ref_school=self.logged_in_user).order_by('first_name')
            self.fields["ref_schedule"].queryset = SchoolSchedule.objects.filter(
                ref_school=self.logged_in_user)
            self.fields["ref_room"].queryset = SchoolRoom.objects.filter(
                ref_school=self.logged_in_user).order_by('name')
            self.fields["ref_type_of_course"].queryset = SchoolCourseType.objects.filter(
                ref_school=self.logged_in_user).order_by('name')
        elif user_type == 'teacher':
            self.fields["ref_level"].queryset = SchoolCourseLevel.objects.filter(
                ref_school__rel_ref_school_school_course__ref_teacher_name=self.logged_in_user)
            self.fields["ref_room"].queryset = SchoolRoom.objects.filter(
                ref_school__rel_ref_school_school_course__ref_teacher_name=self.logged_in_user)

    def clean_title(self):
        return str(self.cleaned_data.get('title')).title()

    def clean_note(self):
        return str(self.cleaned_data.get('note')).title()


class SchoolClassEditForm(forms.ModelForm):

    # ref_course = forms.ModelChoiceField(
    #     widget=forms.Select(
    #         attrs={
    #             'class': 'form-select form-select-lg',
    #             'placeholder': 'Select Course'
    #         }
    #     ),
    #     label="Select Course", label_suffix="",
    #     queryset=SchoolCourse.objects.all(),
    # )

    note = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'course-formset-field form-control form-control-lg text-capitalize', 'rows': 4, 'cols': 10,
        'placeholder': 'Note'
    }), label="Note", label_suffix="", required=False)

    # ref_level = forms.ModelChoiceField(
    # 	label='Level',
    # 	label_suffix="",
    # 	queryset = SchoolCourseLevel.objects.all(),
    # 	widget=forms.RadioSelect(attrs={})
    # 	)
    # ref_room = forms.ModelChoiceField(
    # 	label='Room',
    # 	label_suffix="",
    # 	queryset = SchoolRoom.objects.all(),
    # 	widget=forms.Select(attrs={'class': 'form-select form-select-lg'})
    # 	)
    # type_of_course = forms.ModelChoiceField(
    # 	label='Type',
    # 	label_suffix="",
    # 	queryset = SchoolCourse.objects.only('type_of_course'),
    # 	widget=forms.Select(attrs={'class': 'form-select form-select-lg'})
    # )

    # ref_day = forms.ModelMultipleChoiceField(queryset = WeekDayList.objects.all(), widget=forms.CheckboxSelectMultiple(),)
    class Meta:
        model = SchoolClass
        fields = ('title', 'ref_level',
                  'ref_type_of_course', 'note', 'document')

    def clean_title(self):
        return str(self.cleaned_data.get('title')).title()

    def clean_note(self):
        return str(self.cleaned_data.get('note')).title()

    # def __init__(self, *args, **kwargs):
    # 	print('=>'*10, kwargs)
    # 	if kwargs.get("logged_in_user"):
    # 		self.logged_in_user = kwargs.pop("logged_in_user")
    # 	else:
    # 		self.logged_in_user = kwargs.get("logged_in_user")

    # 	user_type = kwargs.get( "user_type" )
    # 	print("=======================forms==================")
    # 	print(self.logged_in_user)
    # 	super(SchoolCourseForm, self).__init__(*args, **kwargs)

    # 	if user_type == None:
    # 		self.fields["ref_level"].queryset = SchoolCourseLevel.objects.filter(ref_school=self.logged_in_user)
    # 		self.fields["ref_room"].queryset = SchoolRoom.objects.filter(ref_school=self.logged_in_user)
    # 	elif user_type == 'teacher':
    # 		self.fields["ref_level"].queryset = SchoolCourseLevel.objects.filter(ref_school__rel_ref_school_school_course__ref_teacher_name=self.logged_in_user)
    # 		self.fields["ref_room"].queryset = SchoolRoom.objects.filter(ref_school__rel_ref_school_school_course__ref_teacher_name=self.logged_in_user)
    # 	self.fields["ref_teacher_name"].queryset = User.objects.filter(groups__name='teacher')


class SchoolCoursePriceForm(forms.ModelForm):
    class Meta:
        model = SchoolCoursePrice
        fields = ('max_weak', 'min_weak', 'price')
        widgets = {
            'max_weak': forms.TextInput(attrs={'class': 'formset-field form-control form-control-lg course-min-max-price', 'required': True}),
            'min_weak': forms.TextInput(attrs={'class': 'formset-field form-control form-control-lg course-min-max-price', 'required': True}),
            'price': forms.TextInput(attrs={'class': 'formset-field form-control form-control-lg course-min-max-price', 'required': True})
        }
