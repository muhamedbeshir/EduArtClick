from django import forms
from django.utils.translation import gettext_lazy as _
from v1.base.configs import cRequest
from v1.db.master.school_class import SchoolClass

from v1.db.models import SchoolCertificateContent, SchoolCourse


class SchoolCertificateContentForm(forms.ModelForm):
    ref_course = forms.ModelChoiceField(
        label='School Course',
        label_suffix="",
        queryset=SchoolClass.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-select form-select-lg'})
    )

    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg text-uppercase',
        'placeholder': 'Certificate Code'
    }), error_messages={'required': 'School Certificate Code is required !'}, label="Code", label_suffix="")

    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control form-control-lg text-capitalize',
        'cols': "40", 'rows': "5",
        'placeholder': 'Certificate Content'
    }), error_messages={'required': 'School Certificate Content is required !'}, label="Content", label_suffix="")

    class Meta:
        model = SchoolCertificateContent
        fields = ['ref_course', 'code', 'content']

    def __init__(self, *args, **kwargs):
        self.course_id = kwargs.pop('pk', None)
        super(__class__, self).__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields["ref_course"].queryset = SchoolClass.objects.filter(
                ref_course=self.instance.ref_course.ref_course)
            pass
        else:
            self.fields["ref_course"].queryset = SchoolClass.objects.filter(
                ref_course__pk=self.course_id)

    def clean_code(self):
        return str(self.cleaned_data.get('code')).upper()

    def clean_content(self):
        return str(self.cleaned_data.get('content')).title()


class SchoolCertificateContentFormView(forms.ModelForm):
    ref_course = forms.ModelChoiceField(
        label='School Course',
        label_suffix="",
        queryset=SchoolClass.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control form-control-lg'})
    )

    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg'
    }), error_messages={'required': 'School Certificate Code is required !'}, label="Code", label_suffix="")

    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control form-control-lg',
        'cols': "40", 'rows': "5"
    }), error_messages={'required': 'School Certificate Content is required !'}, label="Content", label_suffix="")

    class Meta:
        model = SchoolCertificateContent
        fields = ['ref_course', 'code', 'content']

    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)

        self.fields["ref_course"].queryset = SchoolClass.objects.filter(
            ref_school=cRequest.params.get("school_id")).all()
        self.fields["ref_course"].disabled = True
        self.fields["code"].disabled = True
        self.fields["content"].disabled = True


# class SchoolLetterFormView(forms.ModelForm):

# 	ref_course = forms.ModelChoiceField(
# 		label='School Course',
# 		label_suffix="",
# 		queryset = SchoolCourse.objects.all(),
# 		widget=forms.Select(attrs={'class':'form-control'})
# 		)

# 	is_default = forms.BooleanField(label='Is Default', label_suffix = "",
# 		required=False,
# 		widget=forms.widgets.CheckboxInput(attrs={'class': 'form-check-input'}),
#                                  )
# 	content = forms.CharField(widget=forms.Textarea(attrs={
#          'class': 'form-control'
#      }), error_messages={'required': 'School Letter content is required !'}, label="Letter Content", label_suffix="")

# 	class Meta:
# 		model = SchoolCertificateContent
# 		fields = ['ref_type','is_default','content']

# 	def __init__(self, *args, **kwargs):
# 		super(__class__, self).__init__(*args, **kwargs)

# 		self.fields["ref_type"].disabled = True
# 		self.fields["is_default"].disabled = True
# 		self.fields["content"].disabled = True
