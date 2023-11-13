from django import forms
from v1.db.models import UserAddress

class UserAddressForm(forms.ModelForm):

    class Meta:
        model = UserAddress
        fields = ('street_1','street_2','city','state','code')

    def clean_street_1(self):
        return str(self.cleaned_data['street_1']).title()

    def clean_street_2(self):
        return str(self.cleaned_data['street_2']).title()

    def clean_city(self):
        return str(self.cleaned_data['city']).title()

    def clean_state(self):
        return str(self.cleaned_data['state']).title()