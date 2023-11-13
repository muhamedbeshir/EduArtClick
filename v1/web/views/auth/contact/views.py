from django.shortcuts import render,redirect
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User, Group

from v1.db.models import *
from .forms import *

from django.forms import formset_factory
from django.forms import modelformset_factory
from django.db import transaction, IntegrityError
import phonenumbers


def validateNumber(phone_number, form):
	print('Mobile Number: ', phone_number)
	try:
		validate_number = phonenumbers.parse(phone_number, None)
		if phonenumbers.is_valid_number(validate_number):
			print('Valid Mobile Number: ', phone_number)
			return True
		else:
			print('Invalid Mobile Number: ', phone_number)
			error = f"Please enter a valid mobile number: {phone_number}"
			form.add_error(None, error)
	except phonenumbers.phonenumberutil.NumberParseException:
		print("phonenumbers.phonenumberutil.NumberParseException")
		error = f"Please enter a valid mobile number: {phone_number}"
		form.add_error(None, error)
		print(form.errors)
	
	return False


@login_required
@permission_required(['db.add_usercontact'], raise_exception=True)
def create_teacher_user_contact_by_school(request, pk):
	user=request.user
	raise_permision_denied = False

	if user.groups.filter(name='school').exists():
		logged_in_user = request.user.organizationuserprofile.ref_school.id
		try:
			user = User.objects.get(id=pk)
			_id=user.teacheruserprofile.ref_school.id
			
			if logged_in_user == _id:
				data = request.POST.dict()
				form = UserContactForm(request.POST or None)
				if request.method=='POST':
					if form.is_valid():
						contact = form.save(commit=False)
						home_phone = data.get('home_phone')
						office_phone = data.get('office_phone')
						personal_email = data.get('personal_email')
						work_email = data.get('work_email')
						emergency_name = data.get('emergency_name')
						emergency_phone = data.get('emergency_phone')
						
						''' Checking valid mobile number using phonenumbers '''
						home_phone_validated = True
						office_phone_validated = True
						emergency_phone_validated = True
						
						if home_phone:
							home_phone_validated = validateNumber(home_phone, form)
						if office_phone:
							office_phone_validated = validateNumber(office_phone, form)
						if emergency_phone:
							emergency_phone_validated = validateNumber(emergency_phone, form)

						if home_phone_validated and office_phone_validated and emergency_phone_validated :
							contact.ref_user = user
							contact.save()
							print("Successfully add data")
							return redirect('web:school_teacher_detail', pk=contact.ref_user.teacheruserprofile.id)
					else:
						print("Form is not valid")
						error = "Form is not valid"
						form.add_error(None, error)
				else:
					pass
				
				return render(request, 'auth/contact/create_teacher_user_contact_by_school.html', {'teacher': user.teacheruserprofile.id, 'form': form})	
			else:
				raise_permision_denied = True
		except User.DoesNotExist:
			raise_permision_denied = True

	elif user.groups.filter(name='admin').exists() or user.is_superuser:
		try:
			user = User.objects.get(id=pk)
			_id=user.teacheruserprofile.ref_school.id
			
			if _id:
				data = request.POST.dict()
				form = UserContactForm(request.POST or None)
				if request.method=='POST':
					if form.is_valid():
						contact = form.save(commit=False)
						home_phone = data.get('home_phone')
						office_phone = data.get('office_phone')
						personal_email = data.get('personal_email')
						work_email = data.get('work_email')
						emergency_name = data.get('emergency_name')
						emergency_phone = data.get('emergency_phone')

						''' Checking valid mobile number using phonenumbers '''
						home_phone_validated = True
						office_phone_validated = True
						emergency_phone_validated = True

						if home_phone:
							home_phone_validated = validateNumber(home_phone, form)
						if office_phone:
							office_phone_validated = validateNumber(office_phone, form)
						if emergency_phone:
							emergency_phone_validated = validateNumber(emergency_phone, form)

						if home_phone_validated and office_phone_validated and emergency_phone_validated :
							contact.ref_user = user
							contact.save()
							print("Successfully add data")
							return redirect('web:school_teacher_detail', pk=contact.ref_user.teacheruserprofile.id)

						# contact.ref_user = user
						# contact.save()
						# print("Successfully add data")
						# return redirect('web:school_teacher_detail', pk=contact.ref_user.teacheruserprofile.id)
					else:
						print("Form is not valid")
						error = "Form is not valid"
						form.add_error(None, error)
				else:
					pass
				
				return render(request, 'auth/contact/create_teacher_user_contact_by_school.html', {'teacher': user.teacheruserprofile.id, 'form': form})	
			else:
				raise_permision_denied = True
		except User.DoesNotExist:
			raise_permision_denied = True
	else:
		raise_permision_denied = True

	if raise_permision_denied:
		raise PermissionDenied()


@login_required
@permission_required(['db.change_usercontact'], raise_exception=True)
def edit_teacher_user_contact_by_school(request, pk):
	user=request.user
	raise_permision_denied = False

	if user.groups.filter(name='school').exists():
		logged_in_user = request.user.organizationuserprofile.ref_school.id
		try:
			queryset = UserContact.objects.get(id=pk)
			print(queryset)
			print(queryset.personal_email)
			_id=queryset.ref_user.teacheruserprofile.ref_school.id
			
			if logged_in_user == _id:
				data = request.POST.dict()
				form = UserContactForm(instance=queryset)
				if request.method=='POST':
					form = UserContactForm(request.POST, instance=queryset)
					if form.is_valid():
						print(form.cleaned_data)
						home_phone = form.cleaned_data.get('home_phone')
						office_phone = form.cleaned_data.get('office_phone')
						emergency_phone = form.cleaned_data.get('emergency_phone')

						''' Checking valid mobile number using phonenumbers '''
						home_phone_validated = True
						office_phone_validated = True
						emergency_phone_validated = True

						if home_phone:
							home_phone_validated = validateNumber(home_phone, form)
						if office_phone:
							office_phone_validated = validateNumber(office_phone, form)
						if emergency_phone:
							emergency_phone_validated = validateNumber(emergency_phone, form)

						if home_phone_validated and office_phone_validated and emergency_phone_validated :
							form.save()
							print("Successfully update data")
							return redirect('web:school_teacher_detail', pk=queryset.ref_user.teacheruserprofile.id)
					else:
						print("Form is not valid")
						error = "Form is not valid"
						form.add_error(None, error)
				else:
					form = UserContactForm(instance=queryset)
				template_name = 'auth/contact/edit_teacher_user_contact_by_school.html'
				kwvars = {
					'contact':queryset,
					'form': form,
				}
				
				return render(request, template_name, kwvars)	
			else:
				raise_permision_denied = True
		except UserContact.DoesNotExist:
			raise_permision_denied = True

	elif user.groups.filter(name='admin').exists() or user.is_superuser:
		try:
			queryset = UserContact.objects.get(id=pk)
			print(queryset)
			print(queryset.personal_email)
			_id=queryset.ref_user.teacheruserprofile.ref_school.id
			
			if _id:
				data = request.POST.dict()
				form = UserContactForm(instance=queryset)
				if request.method=='POST':
					form = UserContactForm(request.POST, instance=queryset)
					if form.is_valid():
						print(form.cleaned_data)
						home_phone = form.cleaned_data.get('home_phone')
						office_phone = form.cleaned_data.get('office_phone')
						emergency_phone = form.cleaned_data.get('emergency_phone')

						''' Checking valid mobile number using phonenumbers '''
						home_phone_validated = True
						office_phone_validated = True
						emergency_phone_validated = True

						if home_phone:
							home_phone_validated = validateNumber(home_phone, form)
						if office_phone:
							office_phone_validated = validateNumber(office_phone, form)
						if emergency_phone:
							emergency_phone_validated = validateNumber(emergency_phone, form)

						if home_phone_validated and office_phone_validated and emergency_phone_validated :
							form.save()
							print("Successfully update data")
							return redirect('web:school_teacher_detail', pk=queryset.ref_user.teacheruserprofile.id)
					else:
						print("Form is not valid")
						error = "Form is not valid"
						form.add_error(None, error)
				else:
					form = UserContactForm(instance=queryset)
				template_name = 'auth/contact/edit_teacher_user_contact_by_school.html'
				kwvars = {
					'contact':queryset,
					'form': form,
				}
				
				return render(request, template_name, kwvars)	
			else:
				raise_permision_denied = True
		except UserContact.DoesNotExist:
			raise_permision_denied = True
	else:
		raise_permision_denied = True

	if raise_permision_denied:
		raise PermissionDenied()


@login_required
@permission_required(['db.delete_usercontact'], raise_exception=True)
def delete_teacher_user_contact_by_school(request, pk):
	user=request.user
	raise_permision_denied = False

	if user.groups.filter(name='school').exists():
		logged_in_user = request.user.organizationuserprofile.ref_school.id
		print(logged_in_user)
		try:
			contact = UserContact.objects.get(id=pk)
			_id=contact.ref_user.teacheruserprofile.ref_school.id
			
			if logged_in_user==_id:
				if request.method == 'POST':
					contact.delete()
					print("Delete Successfully")
					return redirect('web:school_teacher_detail', pk=contact.ref_user.teacheruserprofile.id)
				else:
					pass
				return render(request, 'auth/contact/delete_teacher_user_contact_by_school.html', {'contact': contact})
			else:
				print("==============================auth error===========")
				raise_permision_denied = True

		except:
			print("==============================try error===========")
			raise_permision_denied = True

	elif user.groups.filter(name='admin').exists() or user.is_superuser:
		try:
			contact = UserContact.objects.get(id=pk)
			_id=contact.ref_user.teacheruserprofile.ref_school.id
			
			if _id:
				if request.method == 'POST':
					contact.delete()
					print("Delete Successfully")
					return redirect('web:school_teacher_detail', pk=contact.ref_user.teacheruserprofile.id)
				else:
					pass
				return render(request, 'auth/contact/delete_teacher_user_contact_by_school.html', {'contact': contact})
			else:
				print("==============================auth error===========")
				raise_permision_denied = True

		except:
			print("==============================try error===========")
			raise_permision_denied = True

	else:
		print("==============================groups error===========")
		raise_permision_denied = True

	if raise_permision_denied:
		raise PermissionDenied()

