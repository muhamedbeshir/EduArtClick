from django import forms
from v1.db.school.school_setting import SchoolSetting


class SchoolSettingForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control form-control-lg text-capitalize',
            'placeholder': 'School Name'
        }), error_messages={'required': 'School Name is required !'}, label="Name", label_suffix="")

    class Meta:
        model = SchoolSetting
        fields = ['name', 'logo']

    def clean_name(self):
        return str(self.cleaned_data['name']).title()