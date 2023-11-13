from django import forms
from django.utils.translation import gettext_lazy as _
from v1.db.models import SchoolAccommodationAccBank




class SchoolAccommodationAccBankForm(forms.ModelForm):

    acc_bank = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'course-formset-field form-control form-control-lg text-capitalize',
            'placeholder': 'Bank Name'
        }), label="Acc Bank", label_suffix="")
    acc_holder = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'course-formset-field form-control form-control-lg text-capitalize',
            'placeholder': 'Account Holder Name'
        }), label="Acc Holder", label_suffix="")
    acc_no = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'course-formset-field form-control form-control-lg text-capitalize',
            'placeholder': 'Account Number'
        }), label="Acc No", label_suffix="")
    bank_sort_code = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'course-formset-field form-control form-control-lg text-uppercase',
            'placeholder': 'Bank IFSC Code'
        }), label="Bank sort code", label_suffix="")

    class Meta:
        model = SchoolAccommodationAccBank
        fields = ('acc_bank','acc_holder','acc_no','bank_sort_code')



