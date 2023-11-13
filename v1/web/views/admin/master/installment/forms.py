from django import forms
from v1.db.master.school_class_installment import SchoolClassInstallment


class SchoolClassInstallmentForm(forms.ModelForm):

    class Meta:
        model = SchoolClassInstallment
        fields = ('type', 'charges',)

    def __init__(self, *args, **kwargs):
        super(SchoolClassInstallmentForm, self).__init__(*args, **kwargs)

        self.fields['type'].widget.attrs.update(
            {'class': 'form-select form-select-lg'})
        self.fields['charges'].widget.attrs.update(
            {'class': 'form-control form-control-lg', 'min': 0, 'max': 100})
