from django import forms
from django.contrib.auth.models import Group


class GroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ('name',)


    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({
            'class': 'form-control text-lowercase', 
            'placeholder': 'Group Name',
            # 'pattern': '[A-Za-z][A-Za-z0-9\s]+',
        })

    def clean_name(self):
        return str(self.cleaned_data['name']).lower()