from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from django.shortcuts import get_object_or_404
from django.utils import timezone
from v1.db.master.class_classroom import ClassClassroom
from v1.db.master.school_class import SchoolClass
from v1.db.master.school_course import SchoolCourse
from v1.db.master.class_time_table import ClassTimeTable
from v1.db.master.school_room import SchoolRoom
from v1.db.master.school_schedule import SchoolSchedule
from v1.db.user.profile import TeacherUserProfile


class ClassTimeTableForm(forms.ModelForm):

    class Meta:
        model = ClassTimeTable
        fields = ('ref_class', 'class_date', 'start_time', 'end_time',)
        widgets = {
            'class_date': forms.DateInput(attrs={'class': 'form-control form-control-lg', 'type': 'date', 'min': timezone.now().date()}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control form-control-lg', 'type': 'time', }),
            'end_time': forms.TimeInput(attrs={'class': 'form-control form-control-lg', 'type': 'time', }),
        }

    def __init__(self, *args, **kwargs):
        self.course_id = kwargs.pop('course_id', None)
        super(__class__, self).__init__(*args, **kwargs)

        self.fields['ref_class'].widget.attrs.update(
            {'class': 'form-select form-select-lg'})

        if self.instance.pk:
            self.fields['ref_class'].queryset = SchoolClass.objects.filter(
                ref_course=self.instance.ref_course)
        else:
            self.fields['ref_class'].queryset = SchoolClass.objects.filter(
                ref_course__pk=self.course_id)
            pass

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()

        start_time = cleaned_data['start_time']
        end_time = cleaned_data['end_time']

        if start_time and end_time and end_time <= start_time:
            raise forms.ValidationError(
                'End time should be greater than start time.')

        return cleaned_data


class ClasssTimeTableForm(forms.ModelForm):

    start_date = forms.DateField()
    end_date = forms.DateField()

    class Meta:
        model = ClassClassroom
        fields = ('ref_schedule', 'ref_teacher', 'ref_room', 'start_date', 'end_date', 'note')


    def __init__(self, *args, **kwargs):
        self.class_id = kwargs.pop('class_id', None)
        super(__class__, self).__init__(*args, **kwargs)

        self.fields['note'].widget.attrs.update(
            {'class': 'form-control form-control-lg' ,'rows': 3})
        self.fields['ref_schedule'].widget.attrs.update(
            {'class': 'form-select form-select-lg'})
        self.fields['ref_room'].widget.attrs.update(
            {'class': 'form-select form-select-lg'})
        self.fields['ref_teacher'].widget.attrs.update(
            {'class': 'form-select form-select-lg'})
        self.fields['start_date'].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd',
                'class': 'form-control form-control-lg',
                }
            )
        self.fields['end_date'].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd',
                'class': 'form-control form-control-lg',
                }
            )

        if self.instance.pk:
            self.fields['ref_schedule'].queryset = SchoolSchedule.objects.filter(
                ref_school=self.instance.ref_class.ref_school)
            self.fields['ref_room'].queryset = SchoolRoom.objects.filter(
                ref_school=self.instance.ref_class.ref_school)
            # self.fields['ref_teacher'].queryset = TeacherUserProfile.objects.filter(
            #     ref_school=self.instance.ref_class.ref_school)
        else:
            classs = get_object_or_404(SchoolClass, pk=self.class_id)
            self.fields['ref_schedule'].queryset = SchoolSchedule.objects.filter(
                ref_school=classs.ref_school)#.exclude(pk=classs.ref_schedule.pk)
            self.fields['ref_room'].queryset = SchoolRoom.objects.filter(
                ref_school=classs.ref_school)#.exclude(pk=classs.ref_room.pk)
            # self.fields['ref_teacher'].queryset = TeacherUserProfile.objects.filter(
            #     ref_school=classs.ref_school)#.exclude(pk=classs.ref_room.pk)

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()

        start_date = cleaned_data['start_date']
        end_date = cleaned_data['end_date']

        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError(
                'End date should be greater than start date.')

        return cleaned_data
