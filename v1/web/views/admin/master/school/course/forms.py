from django import forms
from django.utils.translation import gettext_lazy as _
from v1.db.models import SchoolRoom, SchoolCourse, SchoolCoursePrice, SchoolCourseLevel, SchoolCourseType, WeekDayList
from django.contrib.auth.models import User, Group

from v1.db.models import TeacherUserProfile
from v1.web.views.admin.master import teacher



class SchoolCourseForm(forms.ModelForm):

	title = forms.CharField(widget=forms.TextInput(attrs={
         'class': 'course-formset-field form-control form-control-lg text-capitalize',
		 'placeholder': 'Course Name'
	}), label="Course Name", label_suffix="")

	class Meta:
		model = SchoolCourse
		fields = ('title',)

	def __init__(self, *args, **kwargs):
		print('=>'*10, kwargs)
		if kwargs.get("logged_in_user"):
			self.logged_in_user = kwargs.pop("logged_in_user")
		else:
			self.logged_in_user = kwargs.get("logged_in_user")

		user_type = kwargs.get( "user_type" )
		print("=======================forms==================")
		print(self.logged_in_user)
		super(SchoolCourseForm, self).__init__(*args, **kwargs)

	def clean_title(self):
		return str(self.cleaned_data.get('title')).title()

class SchoolCourseEditForm(forms.ModelForm):

	title = forms.CharField(widget=forms.TextInput(attrs={
         'class': 'course-formset-field form-control form-control-lg text-capitalize',
		 'placeholder': 'Course Name'
     }), label="Course Name", label_suffix="")

	class Meta:
		model = SchoolCourse
		fields = ('title', )

	def clean_title(self):
		return str(self.cleaned_data.get('title')).title()

	
	def __init__(self, *args, **kwargs):
		print('=>'*10, kwargs)
		if kwargs.get("logged_in_user"):
			self.logged_in_user = kwargs.pop("logged_in_user")
		else:
			self.logged_in_user = kwargs.get("logged_in_user")

		user_type = kwargs.get( "user_type" )
		print("=======================forms==================")
		print(self.logged_in_user)
		super(SchoolCourseForm, self).__init__(*args, **kwargs)


class SchoolCoursePriceForm(forms.ModelForm):
	class Meta:
		model = SchoolCoursePrice
		fields = ('max_weak', 'min_weak', 'price')
		widgets = {
			'max_weak': forms.TextInput(attrs={'class': 'formset-field form-control form-control-lg course-min-max-price', 'required': True}),
			'min_weak': forms.TextInput(attrs={'class': 'formset-field form-control form-control-lg course-min-max-price', 'required': True}),
			'price': forms.TextInput(attrs={'class': 'formset-field form-control form-control-lg course-min-max-price', 'required': True})
		}