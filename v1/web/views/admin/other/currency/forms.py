from django import forms
from django.utils.translation import gettext_lazy as _
from v1.db.models import Currency



class CurrencyForm(forms.ModelForm):

    title = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'formset-field form-control form-control-lg text-capitalize', 'required':'required'
        }), error_messages={'required': 'Title name is required !'}, label="Title", label_suffix="")
    currency_short = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'formset-field form-control form-control-lg text-uppercase', 'required':'required'
        }), error_messages={'required': 'Currency Code name is required !'}, label="Currency Code", label_suffix="")
    currency_symbol = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'formset-field form-control form-control-lg text-uppercase'
        }), label="Currency Symbol", label_suffix="", required=False)

    class Meta:
        model = Currency
        fields = ['title','currency_short', 'currency_symbol']

    def clean_title(self):
        return str(self.cleaned_data['title']).title()

    def clean_currency_short(self):
        return str(self.cleaned_data['currency_short']).upper()

    def clean_currency_symbol(self):
        return str(self.cleaned_data['currency_symbol']).upper()
