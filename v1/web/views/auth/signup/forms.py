from django import forms
from django.contrib.auth.models import User
from v1.db.models import School, UserProfile, StudentUserProfile, AggentUserProfile, Organization, OrganizationUserProfile, TeacherUserProfile, SchoolStudentUserProfile

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput(attrs={
         'class': 'form-control form-control-lg'
     }), error_messages={'required': 'Please enter  Password !'}, label="Password", label_suffix="")
	email = forms.CharField(widget=forms.EmailInput(attrs={
         'class': 'form-control form-control-lg'
     }), error_messages={'required': 'Please enter  Email !'}, label="Email", label_suffix="")

	class Meta:
          model = UserProfile
          exclude = ('ref_user',)
          fields = '__all__'

class UpdateUserForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        exclude = ('ref_user','username')
        fields = '__all__'


class SignUpForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg text-capitalize', 'placeholder': 'First name', 'autocomplete':'off'
    }), label="First name", label_suffix="")
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg text-capitalize', 'placeholder': 'Last name', 'autocomplete':'off'
    }), label="Last name", label_suffix="")
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control form-control-lg'
    }), error_messages={'required': 'Please enter Email !'}, label="Email", label_suffix="")

    class Meta:
        model = UserProfile
        exclude = ('ref_user',)
        fields = '__all__'

    def clean_first_name(self):
        return str(self.cleaned_data['first_name']).title()

    def clean_last_name(self):
        return str(self.cleaned_data['last_name']).title()

class EditSignUpForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg text-capitalize', 'placeholder': 'First name', 'autocomplete':'off'
    }), label="First name", label_suffix="")
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg text-capitalize', 'placeholder': 'Last name', 'autocomplete':'off'
    }), label="Last name", label_suffix="")

    class Meta:
        model = UserProfile
        exclude = ('ref_user',)
        fields = ('first_name', 'last_name')

    
    def clean_first_name(self):
        return str(self.cleaned_data['first_name']).title()

    def clean_last_name(self):
        return str(self.cleaned_data['last_name']).title()


class StudentSignUpForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg text-capitalize', 'placeholder': 'First name', 'autocomplete':'off'
    }), label="First name", label_suffix="")
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg text-capitalize', 'placeholder': 'Last name', 'autocomplete':'off'
    }), label="Last name", label_suffix="")
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control form-control-lg'
    }), error_messages={'required': 'Please enter  Email !'}, label="Email", label_suffix="")

    class Meta:
        model = StudentUserProfile
        exclude = ('ref_user',)
        fields = '__all__'

    def clean_first_name(self):
        return str(self.cleaned_data['first_name']).title()

    def clean_last_name(self):
        return str(self.cleaned_data['last_name']).title()

class EditStudentSignUpForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg text-capitalize', 'placeholder': 'First name', 'autocomplete':'off'
    }), label="First name", label_suffix="")
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg text-capitalize', 'placeholder': 'Last name', 'autocomplete':'off'
    }), label="Last name", label_suffix="")

    class Meta:
        model = StudentUserProfile
        exclude = ('ref_user',)
        fields = ('first_name', 'last_name')
          

    def clean_first_name(self):
        return str(self.cleaned_data['first_name']).title()

    def clean_last_name(self):
        return str(self.cleaned_data['last_name']).title()

class AgentSignUpForm(forms.ModelForm):

    company_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg text-capitalize', 'placeholder': 'Company name', 'autocomplete':'off'
    }), label="First name", label_suffix="")
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg text-capitalize', 'placeholder': 'First name', 'autocomplete':'off'
    }), label="First name", label_suffix="")
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg text-capitalize', 'placeholder': 'Last name', 'autocomplete':'off'
    }), label="Last name", label_suffix="")
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control form-control-lg', 'placeholder': 'Email'
    }), error_messages={'required': 'Please enter  Email !'}, label="Email", label_suffix="")

    class Meta:
        model = AggentUserProfile
        exclude = ('ref_user',)
        fields = '__all__'


    def clean_company_name(self):
        return str(self.cleaned_data['company_name']).title()

    def clean_first_name(self):
        return str(self.cleaned_data['first_name']).title()

    def clean_last_name(self):
        return str(self.cleaned_data['last_name']).title()

class EditAgentSignUpForm(forms.ModelForm):

    company_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg text-capitalize', 'placeholder': 'Company name', 'autocomplete':'off'
    }), label="First name", label_suffix="")
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg text-capitalize', 'placeholder': 'First name', 'autocomplete':'off'
    }), label="First name", label_suffix="")
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg text-capitalize', 'placeholder': 'Last name', 'autocomplete':'off'
    }), label="Last name", label_suffix="")

    class Meta:
        model = AggentUserProfile
        exclude = ('ref_user',)
        fields = ('company_name', 'first_name', 'last_name')

    
    def clean_company_name(self):
        return str(self.cleaned_data['company_name']).title()

    def clean_first_name(self):
        return str(self.cleaned_data['first_name']).title()

    def clean_last_name(self):
        return str(self.cleaned_data['last_name']).title()


class OrganizationSignUpForm(forms.ModelForm):
    ref_organization = forms.ModelChoiceField(
        label='Organization',
        queryset=Organization.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class':'form-select form-select-lg'}),
    )
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg text-capitalize', 'placeholder': 'First name', 'autocomplete':'off'
    }), label="First name", label_suffix="")
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg text-capitalize', 'placeholder': 'Last name', 'autocomplete':'off'
    }), label="Last name", label_suffix="")
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control form-control-lg', 'placeholder': 'Email'
    }), error_messages={'required': 'Please enter  Email !'}, label="Email", label_suffix="")

    class Meta:
        model = OrganizationUserProfile
        exclude = ('ref_user',)
        fields = '__all__'


    def clean_first_name(self):
        return str(self.cleaned_data['first_name']).title()

    def clean_last_name(self):
        return str(self.cleaned_data['last_name']).title()

class EditOrganizationSignUpForm(forms.ModelForm):
    ref_organization = forms.ModelChoiceField(
        label='Organization',
        queryset=Organization.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class':'form-select form-select-lg'}),
    )
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg text-capitalize', 'placeholder': 'First name', 'autocomplete':'off'
    }), label="First name", label_suffix="")
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg text-capitalize', 'placeholder': 'Last name', 'autocomplete':'off'
    }), label="Last name", label_suffix="")

    class Meta:
        model = OrganizationUserProfile
        exclude = ('ref_user',)
        fields = ('ref_organization', 'first_name', 'last_name')


    def clean_first_name(self):
        return str(self.cleaned_data['first_name']).title()

    def clean_last_name(self):
        return str(self.cleaned_data['last_name']).title()


class SchoolOrganizationSignUpForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg text-capitalize', 'placeholder': 'First name', 'autocomplete':'off'
    }), label="First name", label_suffix="")
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg text-capitalize', 'placeholder': 'Last name', 'autocomplete':'off'
    }), label="Last name", label_suffix="")
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control form-control-lg', 'placeholder': 'Email'
    }), error_messages={'required': 'Please enter  Email !'}, label="Email", label_suffix="")

    class Meta:
        model = OrganizationUserProfile
        exclude = ('ref_user','ref_organization')
        fields = '__all__'


    def clean_first_name(self):
        return str(self.cleaned_data['first_name']).title()

    def clean_last_name(self):
        return str(self.cleaned_data['last_name']).title()
    

class SchoolTeacherSignUpForm(forms.ModelForm):

    class Meta:
        model = TeacherUserProfile
        exclude = ('ref_user','ref_school')
        fields = ('first_name', 'last_name', 'gender', 'date_of_birth', 'lang_one', 'lang_two','lang_three', 'avtar')

    def clean_first_name(self):
        return str(self.cleaned_data['first_name']).title()

    def clean_last_name(self):
        return str(self.cleaned_data['last_name']).title()

    def clean_lang_one(self):
        return str(self.cleaned_data['lang_one']).title()

    def clean_lang_two(self):
        return str(self.cleaned_data['lang_two']).title()

    def clean_lang_three(self):
        return str(self.cleaned_data['lang_three']).title()



class SchoolStudentSignUpForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
         'class': 'form-control form-control-lg text-capitalize', 'placeholder': 'First Name', 'autocomplete':'off'
     }), label="First name", label_suffix="")
    last_name = forms.CharField(widget=forms.TextInput(attrs={
         'class': 'form-control form-control-lg text-capitalize', 'placeholder': 'Last Name', 'autocomplete':'off'
     }), label="First name", label_suffix="")
   
    class Meta:
        model = SchoolStudentUserProfile
        exclude = ('ref_user','ref_school')
        fields = ('first_name', 'last_name', 'gender', 'date_of_birth','home_address', 'post_code','nationality', 'phone', 'religion', 'passport_number', 'passport_expiry_date','avtar')

    def clean_first_name(self):
        return str(self.cleaned_data['first_name']).title()

    def clean_last_name(self):
        return str(self.cleaned_data['last_name']).title()

    def clean_home_address(self):
        return str(self.cleaned_data['home_address']).title()

    def clean_nationality(self):
        return str(self.cleaned_data['nationality']).title()

    def clean_religion(self):
        return str(self.cleaned_data['religion']).title()

    def clean_passport_number(self):
        return str(self.cleaned_data['passport_number']).upper()



class SchoolSignUpForm(forms.ModelForm):
    ref_organization = forms.ModelChoiceField(
        label='Organization',
        queryset=Organization.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class':'form-select form-select-lg'}),
    )
    ref_school = forms.ModelChoiceField(
        label='Organization',
        queryset=School.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class':'form-select form-select-lg'}),
    )
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg text-capitalize', 'placeholder': 'First name', 'autocomplete':'off'
    }), label="First name", label_suffix="")
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg text-capitalize', 'placeholder': 'Last name', 'autocomplete':'off'
    }), label="Last name", label_suffix="")
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control form-control-lg', 'placeholder': 'Email'
    }), error_messages={'required': 'Please enter  Email !'}, label="Email", label_suffix="")

    class Meta:
        model = OrganizationUserProfile
        exclude = ('ref_user',)
        fields = '__all__'

    
    def clean_first_name(self):
        return str(self.cleaned_data['first_name']).title()

    def clean_last_name(self):
        return str(self.cleaned_data['last_name']).title()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ref_school'].queryset = School.objects.none()

        if 'ref_organization' in self.data:
            try:
                organization_id = int(self.data.get('ref_organization'))
                self.fields['ref_school'].queryset = School.objects.filter(ref_organization=organization_id).order_by('school_name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            print(self.instance.pk)
            self.fields['ref_school'].queryset = self.instance.ref_school.ref_organization.rel_ref_organization_organization.order_by('school_name')

class EditSchoolSignUpForm(forms.ModelForm):
    ref_organization = forms.ModelChoiceField(
        label='Organization',
        queryset=Organization.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class':'form-select form-select-lg'}),
    )
    ref_school = forms.ModelChoiceField(
        label='Organization',
        queryset=School.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class':'form-select form-select-lg'}),
    )
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg text-capitalize', 'placeholder': 'First name', 'autocomplete':'off'
    }), label="First name", label_suffix="")
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg text-capitalize', 'placeholder': 'Last name', 'autocomplete':'off'
    }), label="Last name", label_suffix="")

    class Meta:
        model = OrganizationUserProfile
        exclude = ('ref_user',)
        fields = ('ref_organization', 'ref_school', 'first_name', 'last_name')

    
    def clean_first_name(self):
        return str(self.cleaned_data['first_name']).title()

    def clean_last_name(self):
        return str(self.cleaned_data['last_name']).title()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    #   self.fields['ref_school'].queryset = School.objects.none()

        if 'ref_organization' in self.data:
            try:
                organization_id = int(self.data.get('ref_organization'))
                self.fields['ref_school'].queryset = School.objects.filter(ref_organization=organization_id).order_by('school_name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            print(self.instance.pk)
            self.fields['ref_school'].queryset = self.instance.ref_school.ref_organization.rel_ref_organization_organization.order_by('school_name')
