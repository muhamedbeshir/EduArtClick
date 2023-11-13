from django import forms
from django.utils import timezone


from django.utils.translation import gettext_lazy as _
from v1.db.master.school_class import SchoolClass
from v1.db.models import SchoolRoom, SchoolCourse, SchoolCoursePrice, SchoolCourseLevel, SchoolCourseType
from django.contrib.auth.models import User, Group

from v1.db.models import SchoolExamType, SchoolCourse, SchoolExam, SchoolExamCategory, SchoolExamQuestions, TeacherUserProfile
from v1.base.configs import cRequest


class SchoolExamForm(forms.ModelForm):
    ref_exam_type = forms.ModelChoiceField(queryset=SchoolExamType.objects.all(
    ),  widget=forms.Select(attrs={'class': 'form-select form-select-lg'}))
    ref_course = forms.ModelChoiceField(queryset=SchoolClass.objects.none(
    ), widget=forms.Select(attrs={'class': 'form-select form-select-lg'}))

    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'exam-formset-field form-control form-control-lg text-capitalize',
        'placeholder': 'Course Name',
    }), label="Exam Name", label_suffix="")

    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'exam-formset-field form-control form-control-lg text-uppercase',
        'placeholder': 'Exam Code',
    }), label="Note", label_suffix="", required=True)

    duration = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'exam-formset-field form-control form-control-lg', 'placeholder': 'In Minutes'
    }), label="Exam Duration", label_suffix="", required=True)

    score = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'exam-formset-field form-control form-control-lg',
        'placeholder': 'Exam Score',
    }), label="Exam Score", label_suffix="", required=True)

    total_questions = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'exam-formset-field form-control form-control-lg',
        'placeholder': 'Total Questions',
    }), label="Exam Total Questions", label_suffix="", required=True)

    exam_date = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'form-control form-control-lg', 'type': 'date', 'min': timezone.now().date(),
    }), label='Exam Date', label_suffix='', required=False)

    class Meta:
        model = SchoolExam
        fields = ('ref_exam_type', 'ref_course', 'title',
                  'code', 'duration', 'score', 'total_questions', 'exam_date')

    def __init__(self, *args, **kwargs):
        self.course_id = kwargs.pop("course_id", None)
        super(__class__, self).__init__(*args, **kwargs)

        if self.course_id:
            self.fields["ref_course"].queryset = SchoolClass.objects.filter(
                ref_course__pk=self.course_id)

    def clean_title(self):
        return str(self.cleaned_data['title']).title()

    def clean_code(self):
        return str(self.cleaned_data['code']).upper()


class SchoolExamCategoryForm(forms.ModelForm):
    class Meta:
        model = SchoolExamCategory
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'formset-field form-control'})
        }


class SchoolExamQuestionsForm(forms.ModelForm):
    class Meta:
        model = SchoolExamQuestions
        fields = ('ref_exam_category', 'question', 'answer',
                  'option1', 'option2', 'option3', 'score')
        widgets = {
            'question': forms.TextInput(attrs={'class': 'formset-field form-control'}),

            'answer': forms.TextInput(attrs={'class': 'formset-field form-control'}),
            'option1': forms.TextInput(attrs={'class': 'formset-field form-control'}),
            'option2': forms.TextInput(attrs={'class': 'formset-field form-control'}),
            'option3': forms.TextInput(attrs={'class': 'formset-field form-control'}),

            'score': forms.TextInput(attrs={'class': 'formset-field form-control'}),
        }
