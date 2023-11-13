from django.utils import timezone
from django import forms
from v1.base.configs import cRequest
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from v1.db.master.school_class import SchoolClass
from v1.db.master.school_course import SchoolCourse
from v1.db.school.school_exam import SchoolExam

from v1.db.school.school_sslue import SelectiveStudentExam
from v1.db.user.profile import SchoolStudentUserProfile
from v1.db.user.student_profile_has_course import StudentProfileHasCourse


class SelectiveStudentExamForm(forms.ModelForm):

    class Meta:
        model = SelectiveStudentExam
        fields = ['ref_course', 'ref_exam']

    def __init__(self, *args, **kwargs):
        self.course_id = kwargs.pop('course_id', None)
        super(__class__, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-select form-select-lg'})

        if self.course_id:
            self.fields['ref_course'].queryset = SchoolClass.objects.filter(ref_course__pk=self.course_id)
            self.fields['ref_exam'].queryset = SchoolExam.objects.filter(ref_course__pk=self.course_id)

