from django import forms
from django.utils.translation import gettext_lazy as _
from v1.db.models import SchoolExamQuestions , SchoolExamCategory

from v1.base.configs import cRequest

from django.forms import formset_factory
from django.forms import modelformset_factory

class SchoolExamQuestionsForm(forms.ModelForm):
    ref_exam_category = forms.ModelChoiceField(queryset = SchoolExamCategory.objects.all(),  widget=forms.Select(attrs={'class':'form-control formset-field'}))

    question = forms.CharField(widget=forms.TextInput(attrs={
         'class': 'form-control formset-field'
     }), error_messages={'required': 'School Exam Question is required !'}, label="Exam Question", label_suffix="")

    answer = forms.CharField(widget=forms.TextInput(attrs={
         'class': 'form-control formset-field'
     }), error_messages={'required': 'School Exam Answer is required !'}, label="Exam Question Answer", label_suffix="")

    option1 = forms.CharField(widget=forms.TextInput(attrs={
         'class': 'form-control formset-field'
     }), error_messages={'required': 'School Exam Option 1 is required !'}, label="Exam Question Option 1", label_suffix="")

    option2 = forms.CharField(widget=forms.TextInput(attrs={
         'class': 'form-control formset-field'
     }), error_messages={'required': 'School Exam Option 2 is required !'}, label="Exam Question Option 2", label_suffix="")

    option3 = forms.CharField(widget=forms.TextInput(attrs={
         'class': 'form-control formset-field'
     }), error_messages={'required': 'School Exam Option 3 is required !'}, label="Exam Question Option 3", label_suffix="")

    score = forms.IntegerField(widget=forms.TextInput(attrs={
         'class': 'form-control formset-field'
     }), error_messages={'required': 'School Exam Score is required !'}, label="Exam Score", label_suffix="")

    class Meta:
        model = SchoolExamQuestions 
        fields = ['ref_exam_category','question' , 'answer' , 'option1' , 'option2' , 'option3' , 'score']

    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)

        self.fields["ref_exam_category"].queryset = SchoolExamCategory.objects.filter(ref_exam=cRequest.params.get( "ref_exam_id" )).all()

ExamQuestionsFormset = modelformset_factory(SchoolExamQuestions, form=SchoolExamQuestionsForm)