from django import forms
from v1.db.models import CertificateTeacher

class CertificateTeacherForm(forms.ModelForm):

    class Meta:
        model = CertificateTeacher
        fields = ('name','code','date')

    def clean_name(self):
        return str(self.cleaned_data['name']).title()

    def clean_code(self):
        return str(self.cleaned_data['code']).upper()