from django import forms
from django.utils.translation import gettext_lazy as _
from v1.db.master.school_course_level import SchoolCourseLevel
from v1.db.models import SchoolExamResult


class SchoolExamResultForm(forms.ModelForm):
    remarks = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg'
    }), label="Exam Result Remarks", label_suffix="")

    ref_course_level = forms.ModelChoiceField(queryset=SchoolCourseLevel.objects.all(
    ),  widget=forms.Select(attrs={'class': 'form-select form-select-lg'}))

    class Meta:
        model = SchoolExamResult
        fields = ['remarks', 'ref_course_level']

    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)
        if kwargs['instance'].ref_application:
            school_id = kwargs['instance'].ref_application.ref_school.id
        if kwargs['instance'].ref_school_student:
            school_id = kwargs['instance'].ref_school_student.ref_school.id

        self.fields["ref_course_level"].queryset = SchoolCourseLevel.objects.filter(
            ref_school=school_id).all()
