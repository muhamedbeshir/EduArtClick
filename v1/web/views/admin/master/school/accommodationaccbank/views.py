from django.shortcuts import render,redirect
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db.models import Avg, Max, Min
from django.core.exceptions import PermissionDenied
from v1.db.models import *

from .forms import *

from django.forms import formset_factory
from django.forms import modelformset_factory
from django.db import transaction, IntegrityError



@login_required
@permission_required(['db.add_schoolaccommodationaccbank'], raise_exception=True)
def create_school_accommodation_acc_bank(request, pk):
	user=request.user
	raise_permision_denied = False

	if user.groups.filter(name='school').exists():
		logged_in_user = request.user.organizationuserprofile.ref_school.id
		try:
			accommodation = SchoolAccommodationOwner.objects.get(id=pk)
			if logged_in_user == accommodation.ref_school.id:

				accommodation = SchoolAccommodationOwner.objects.filter(pk=pk)
				accommodation = accommodation.first()
				context = {}
				form = SchoolAccommodationAccBankForm(request.POST or None)
				data = request.POST.dict()
				if request.method=='POST':
					if form.is_valid():
						#name = data.get('name')
						accommodation_acc_bank = form.save(commit=False)
						accommodation_acc_bank.ref_accommodation = accommodation
						accommodation_acc_bank.save()
						return redirect('web:detail_school_accommodation_owner', pk=accommodation.id)
					else:
						print("Form is not valid")
						error = "Form is not valid"
						form.add_error(None, error)

				context['accommodation'] = accommodation
				context['form'] = form
				return render(request, 'admin/master/accommodationaccbank/create_school_accommodation_acc_bank.html', context)
			else:
				raise_permision_denied = True

		except SchoolAccommodationService.DoesNotExist:
			raise_permision_denied = True

	elif user.groups.filter(name='admin').exists() or user.is_superuser:
		try:
			accommodation = SchoolAccommodationOwner.objects.get(id=pk)
			if accommodation.ref_school.id:

				accommodation = SchoolAccommodationOwner.objects.filter(pk=pk)
				accommodation = accommodation.first()
				context = {}
				form = SchoolAccommodationAccBankForm(request.POST or None)
				data = request.POST.dict()
				if request.method=='POST':
					if form.is_valid():
						#name = data.get('name')
						accommodation_acc_bank = form.save(commit=False)
						accommodation_acc_bank.ref_accommodation = accommodation
						accommodation_acc_bank.save()
						return redirect('web:detail_school_accommodation_owner', pk=accommodation.id)
					else:
						print("Form is not valid")
						error = "Form is not valid"
						form.add_error(None, error)

				context['accommodation'] = accommodation
				context['form'] = form
				return render(request, 'admin/master/accommodationaccbank/create_school_accommodation_acc_bank.html', context)
			else:
				raise_permision_denied = True

		except SchoolAccommodationService.DoesNotExist:
			raise_permision_denied = True

	else:
		raise_permision_denied = True

	if raise_permision_denied:
		raise PermissionDenied()


@login_required
@permission_required(['db.change_schoolaccommodationaccbank'], raise_exception=True)
def edit_school_accommodation_acc_bank(request, pk):
	user=request.user
	raise_permision_denied = False

	if user.groups.filter(name='school').exists():
		logged_in_user = request.user.organizationuserprofile.ref_school.id
		try:
			queryset = SchoolAccommodationAccBank.objects.get(id=pk)
			if logged_in_user == queryset.ref_accommodation.ref_school.id:
				data = request.POST.dict()
				form = SchoolAccommodationAccBankForm(instance=queryset)
				if request.method=='POST':
					form = SchoolAccommodationAccBankForm(request.POST, instance=queryset)
					if form.is_valid():
						form.save()
						print("Successfully edit data")
						return redirect('web:detail_school_accommodation_owner', pk=queryset.ref_accommodation.id)
					else:
						print("Form is not valid")
						error = "Form is not valid"
						form.add_error(None, error)
				else:
					form = SchoolAccommodationAccBankForm(instance=queryset)

				template_name = 'admin/master/accommodationaccbank/edit_school_accommodation_acc_bank.html'
				kwvars = {
					'accommodation_acc_bank':queryset,
					'form': form,
				}
				
				return render(request, template_name, kwvars)	
			else:
				raise_permision_denied = True
		except SchoolAccommodationPreferance.DoesNotExist:
			raise_permision_denied = True

	elif user.groups.filter(name='admin').exists() or user.is_superuser:
		try:
			queryset = SchoolAccommodationAccBank.objects.get(id=pk)
			if queryset.ref_accommodation.ref_school.id:
				data = request.POST.dict()
				form = SchoolAccommodationAccBankForm(instance=queryset)
				if request.method=='POST':
					form = SchoolAccommodationAccBankForm(request.POST, instance=queryset)
					if form.is_valid():
						form.save()
						print("Successfully edit data")
						return redirect('web:detail_school_accommodation_owner', pk=queryset.ref_accommodation.id)
					else:
						print("Form is not valid")
						error = "Form is not valid"
						form.add_error(None, error)
				else:
					form = SchoolAccommodationAccBankForm(instance=queryset)

				template_name = 'admin/master/accommodationaccbank/edit_school_accommodation_acc_bank.html'
				kwvars = {
					'accommodation_acc_bank':queryset,
					'form': form,
				}
				
				return render(request, template_name, kwvars)	
			else:
				raise_permision_denied = True
		except SchoolAccommodationPreferance.DoesNotExist:
			raise_permision_denied = True
	else:
		raise_permision_denied = True

	if raise_permision_denied:
		raise PermissionDenied()


@login_required
@permission_required(['db.delete_schoolaccommodationaccbank'], raise_exception=True)
def delete_school_accommodation_acc_bank(request, pk):
	user=request.user
	raise_permision_denied = False

	if user.groups.filter(name='school').exists():
		logged_in_user = request.user.organizationuserprofile.ref_school.id
		#print(logged_in_user)
		try:
			accommodationaccbank = SchoolAccommodationAccBank.objects.get(id=pk)
			_id=accommodationaccbank.ref_accommodation.ref_school.id
			
			if logged_in_user == _id:
				if request.method == 'POST':
					accommodationaccbank.delete()
					print("Delete Successfully")
					return redirect('web:detail_school_accommodation_owner', pk=accommodationaccbank.ref_accommodation.id)
				else:
					pass
				return render(request, 'admin/master/accommodationaccbank/delete_school_accommodation_acc_bank.html', {'accommodationaccbank': accommodationaccbank})
			else:
				print("==============================auth error===========")
				raise_permision_denied = True

		except:
			print("==============================try error===========")
			raise_permision_denied = True

	elif user.groups.filter(name='admin').exists() or user.is_superuser:
		try:
			accommodationaccbank = SchoolAccommodationAccBank.objects.get(id=pk)
			_id=accommodationaccbank.ref_accommodation.ref_school.id
			
			if _id:
				if request.method == 'POST':
					accommodationaccbank.delete()
					print("Delete Successfully")
					return redirect('web:detail_school_accommodation_owner', pk=accommodationaccbank.ref_accommodation.id)
				else:
					pass
				return render(request, 'admin/master/accommodationaccbank/delete_school_accommodation_acc_bank.html', {'accommodationaccbank': accommodationaccbank})
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

