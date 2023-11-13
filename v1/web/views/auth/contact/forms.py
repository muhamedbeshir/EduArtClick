from django import forms
from v1.db.models import UserContact

class UserContactForm(forms.ModelForm):

    class Meta:
        model = UserContact
        fields = ('home_phone','office_phone','personal_email','work_email','emergency_name','emergency_phone')