from django import forms
from django.utils.translation import gettext_lazy as _
from v1.db.models import Commission

class AgentCommissionForm(forms.ModelForm):

    min_application = forms.IntegerField(
	    label='Minimum Application',
	    label_suffix='',
	    widget=forms.widgets.NumberInput(
            attrs={
                'class': 'form-control form-control-lg',
                'min': 1,
                'placeholder': 1,
            }
        ),
    )
    max_application = forms.IntegerField(
	    label='Maximum Application',
	    label_suffix='',
	    widget=forms.widgets.NumberInput(
            attrs={
                'class': 'form-control form-control-lg',
                'min': 1,
                'placeholder': 1,
            }
        ),
    )
    commission_rate = forms.DecimalField(
	    label='Commission Rate',
	    label_suffix='',
	    widget=forms.widgets.NumberInput(
            attrs={
                'class': 'form-control form-control-lg',
                'min': 0,
                'max': 100,
                'step': 0.5,
                'placeholder': 0,
                'onKeyPress': "if(this.value.length==2) return false;",
            }
        ),
    )
    is_active = forms.BooleanField(
        label='Is Active', 
        label_suffix = "",
        required=False,
        widget=forms.widgets.CheckboxInput(
            attrs={'class': 'form-check-input'}),
    )

    class Meta:
        model = Commission
        fields = ['min_application','max_application', 'commission_rate', 'is_active']

