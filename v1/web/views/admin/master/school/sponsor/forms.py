from django import forms
from v1.db.school.school_sponsor import SchoolSponsor


class SchoolSponsorForm(forms.ModelForm):

    class Meta:
        model = SchoolSponsor
        fields = ['name', 'email', 'address', 'status']
        widgets = {
            'status': forms.CheckboxInput()
        }

    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)

        self.fields['status'].widget.attrs.update(
            {'class': 'form-check-input form-check-input-lg', })
        self.fields['name'].widget.attrs.update(
            {'class': 'form-control form-control-lg text-capitalize', 'placeholder': 'Sponsor Name'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control form-control-lg text-lowercase', 'placeholder': 'Sponsor Email'})
        self.fields['address'].widget.attrs.update(
            {'class': 'form-control form-control-lg text-capitalize', 'placeholder': 'Sponsor Address', 'rows': 4, })

    def clean_name(self):
        return str(self.cleaned_data['name']).title()

    def clean_email(self):
        return str(self.cleaned_data['email']).lower()
