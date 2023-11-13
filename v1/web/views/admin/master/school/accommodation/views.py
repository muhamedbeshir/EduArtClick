from django.shortcuts import render,redirect
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db.models import Avg, Max, Min
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from v1.db.models import *

from .forms import *

from django.forms import formset_factory
from django.forms import modelformset_factory
from django.db import transaction, IntegrityError


@login_required
@permission_required(['db.add_schoolaccommodationservice'], raise_exception=True)
def create_school_accommodation_service(request, pk):
	user=request.user
	raise_permission_denied = False

	if user.groups.filter(name='school').exists():
		logged_in_user = request.user.organizationuserprofile.ref_school.id
		try:
			accommodation_owner_id = SchoolAccommodationOwner.objects.get(id=pk)
			if logged_in_user == accommodation_owner_id.ref_school.id:
				accommodation_owner_id = SchoolAccommodationOwner.objects.filter(pk=pk)
				accommodation_owner_id = accommodation_owner_id.first()
				school=School.objects.get(id=accommodation_owner_id.ref_school.id)
				context = {}
				form = SchoolAccommodationServiceForm(request.POST or None)
				data = request.POST.dict()
				if request.method=='POST':
					if form.is_valid():
						room = form.save(commit=False)
						room.ref_accommodation_owner = accommodation_owner_id
						room.ref_school = school
						room.save()

						try:
							owner = get_object_or_404(SchoolAccommodationOwner, id=accommodation_owner_id.id)
							owner.capacity  = owner.capacity + 1
							owner.save()
							print("Save capacity")
						except:
							print("Not Save capacity")
						return redirect('web:detail_school_accommodation_owner', pk=accommodation_owner_id)
					else:
						print("Form is not valid")
						error = "Form is not valid"
						form.add_error(None, error)

				context['accommodation_owner_id'] = accommodation_owner_id
				context['form'] = form
				return render(request, 'admin/master/accommodation/create_accommodation_service.html', context)
			else:
				raise_permission_denied = True
		except School.DoesNotExist:
			raise_permission_denied = True

	elif user.groups.filter(name='admin').exists() or user.is_superuser:
		try:
			accommodation_owner_id = SchoolAccommodationOwner.objects.get(id=pk)
			if accommodation_owner_id.ref_school.id:
				accommodation_owner_id = SchoolAccommodationOwner.objects.filter(pk=pk)
				accommodation_owner_id = accommodation_owner_id.first()
				school=School.objects.get(id=accommodation_owner_id.ref_school.id)
				context = {}
				form = SchoolAccommodationServiceForm(request.POST or None)
				data = request.POST.dict()
				if request.method=='POST':
					if form.is_valid():
						room = form.save(commit=False)
						room.ref_accommodation_owner = accommodation_owner_id
						room.ref_school = school
						room.save()

						try:
							owner = get_object_or_404(SchoolAccommodationOwner, id=accommodation_owner_id.id)
							owner.capacity  = owner.capacity + 1
							owner.save()
							print("Save capacity")
						except:
							print("Not Save capacity")
						return redirect('web:detail_school_accommodation_owner', pk=accommodation_owner_id)
					else:
						print("Form is not valid")
						error = "Form is not valid"
						form.add_error(None, error)

				context['accommodation_owner_id'] = accommodation_owner_id
				context['form'] = form
				return render(request, 'admin/master/accommodation/create_accommodation_service.html', context)
			else:
				raise_permission_denied = True
		except School.DoesNotExist:
			raise_permission_denied = True
	else:
		raise_permission_denied = True
	
	if raise_permission_denied:
		raise PermissionDenied()


@login_required
@permission_required(['db.change_schoolaccommodationservice'], raise_exception=True)
def edit_school_accommodation_service(request, pk):
	user=request.user
	raise_permission_denied = False

	if user.groups.filter(name='school').exists():
		logged_in_user = request.user.organizationuserprofile.ref_school.id
		try:
			queryset = SchoolAccommodationService.objects.get(id=pk)
			if logged_in_user == queryset.ref_school.id:
				school=queryset.ref_school.id
				data = request.POST.dict()
				form = SchoolAccommodationServiceForm(instance=queryset)
				if request.method=='POST':
					form = SchoolAccommodationServiceForm(request.POST, instance=queryset)
					if form.is_valid():
						room = form.save(commit=False)
						room.status = True
						room.save()
						print("Successfully edit data")
						return redirect('web:detail_school_accommodation_owner', pk=queryset.ref_accommodation_owner.id)
					else:
						print("Form is not valid")
						error = "Form is not valid"
						form.add_error(None, error)
						print(form.errors)
				else:
					form = SchoolAccommodationServiceForm(instance=queryset)

				template_name = 'admin/master/accommodation/edit_accommodation_service.html'
				kwvars = {
					'accommodation':queryset,
					'form': form,
				}
				
				return render(request, template_name, kwvars)	
			else:
				raise_permission_denied = True
		except SchoolAccommodationService.DoesNotExist:
			raise_permission_denied = True

	elif user.groups.filter(name='admin').exists() or user.is_superuser:
		try:
			queryset = SchoolAccommodationService.objects.get(id=pk)
			if queryset.ref_school.id:
				school=queryset.ref_school.id
				data = request.POST.dict()
				form = SchoolAccommodationServiceForm(instance=queryset)
				if request.method=='POST':
					form = SchoolAccommodationServiceForm(request.POST, instance=queryset)
					if form.is_valid():
						room = form.save(commit=False)
						room.status = True
						room.save()
						print("Successfully edit data")
						return redirect('web:detail_school_accommodation_owner', pk=queryset.ref_accommodation_owner.id)
					else:
						print("Form is not valid")
						error = "Form is not valid"
						form.add_error(None, error)
						print(form.errors)
				else:
					form = SchoolAccommodationServiceForm(instance=queryset)

				template_name = 'admin/master/accommodation/edit_accommodation_service.html'
				kwvars = {
					'accommodation':queryset,
					'form': form,
				}
				
				return render(request, template_name, kwvars)	
			else:
				raise_permission_denied = True
		except SchoolAccommodationService.DoesNotExist:
			raise_permission_denied = True
	else:
		raise_permission_denied = True

	if raise_permission_denied:
		raise PermissionDenied()


@login_required
@permission_required(['db.delete_schoolaccommodationservice'], raise_exception=True)
def delete_school_accommodation_service(request, pk):
	user=request.user
	raise_permission_denied = False

	if user.groups.filter(name='school').exists():
		logged_in_user = request.user.organizationuserprofile.ref_school.id
		
		try:
			accommodation = SchoolAccommodationService.objects.get(id=pk)
			_id=accommodation.ref_school.id
			
			if logged_in_user==_id:
				if request.method == 'POST':
					accommodation.delete()
					print("Delete Successfully")
					try:
						owner = get_object_or_404(SchoolAccommodationOwner, id=accommodation.ref_accommodation_owner.id)
						owner.capacity  = owner.capacity - 1
						owner.save()
						print("Save capacity")
					except:
						print("Not Save capacity")
					return redirect('web:deatil_school', pk=accommodation.ref_school.id)
				else:
					pass
				return render(request, 'admin/master/accommodation/delete_accommodation_service.html', {'accommodation': accommodation})
			else:
				print("==============================auth error===========")
				raise_permission_denied = True

		except SchoolAccommodationService.DoesNotExist:
			print("==============================try error===========")
			raise_permission_denied = True

	elif user.groups.filter(name='admin').exists() or user.is_superuser:
		try:
			accommodation = SchoolAccommodationService.objects.get(id=pk)
			_id=accommodation.ref_school.id
			
			if _id:
				if request.method == 'POST':
					accommodation.delete()
					try:
						owner = get_object_or_404(SchoolAccommodationOwner, id=accommodation.ref_accommodation_owner.id)
						owner.capacity  = owner.capacity - 1
						owner.save()
						print("Save capacity")
					except:
						print("Not Save capacity")
					return redirect('web:deatil_school', pk=accommodation.ref_school.id)
				else:
					pass
				return render(request, 'admin/master/accommodation/delete_accommodation_service.html', {'accommodation': accommodation})
			else:
				print("==============================auth error===========")
				raise_permission_denied = True

		except SchoolAccommodationService.DoesNotExist:
			print("==============================try error===========")
			raise_permission_denied = True

	else:
		print("==============================groups error===========")
		raise_permission_denied = True
	
	if raise_permission_denied:
		raise PermissionDenied()

