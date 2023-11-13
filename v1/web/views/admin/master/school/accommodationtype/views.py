from django.shortcuts import render,redirect
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db.models import Avg, Max, Min

from v1.db.models import *

from .forms import *

from django.forms import formset_factory
from django.forms import modelformset_factory
from django.db import transaction, IntegrityError



@login_required
def create_school_accommodation_type(request, pk):
	user=request.user
	if user.groups.filter(name='school').exists():
		logged_in_user = request.user.organizationuserprofile.ref_school.id
		try:
			school = School.objects.get(id=pk)
			if logged_in_user == school.id:

				school = School.objects.filter(pk=pk)
				school = school.first()
				context = {}
				form = SchoolAccommodationTypeForm(request.POST or None)
				data = request.POST.dict()
				if request.method=='POST':
					if form.is_valid():
						accommodation_type_name = data.get('accommodation_type_name')
						accommodation_type = form.save(commit=False)
						accommodation_type.ref_school = school
						accommodation_type.save()
						return redirect('web:deatil_school', pk=school.id)
					else:
						print("Form is not valid")
						error = "Form is not valid"
						form.add_error(None, error)

				context['school'] = school
				context['form'] = form
				return render(request, 'admin/master/accommodationtype/create_school_accommodation_type.html', context)
			else:
				permission = "permission"
				return render(request, 'admin/master/accommodationtype/create_school_accommodation_type.html', {'permission': permission})

		except School.DoesNotExist:
			permission = "permission"
			return render(request, 'admin/master/accommodationtype/create_school_accommodation_type.html', {'permission': permission})

	else:
		permission = "permission"
		return render(request, 'admin/master/accommodationtype/create_school_accommodation_type.html', {'permission': permission})


@login_required
def edit_school_accommodation_type(request, pk):
	user=request.user
	if user.groups.filter(name='school').exists():
		logged_in_user = request.user.organizationuserprofile.ref_school.id
		try:
			queryset = SchoolAccommodationType.objects.get(id=pk)
			if logged_in_user == queryset.ref_school.id:
				data = request.POST.dict()
				form = SchoolAccommodationTypeForm(instance=queryset)
				if request.method=='POST':
					form = SchoolAccommodationTypeForm(request.POST, instance=queryset)
					if form.is_valid():
						form.save()
						print("Successfully edit data")
						return redirect('web:deatil_school', pk=queryset.ref_school.id)
					else:
						print("Form is not valid")
						error = "Form is not valid"
						form.add_error(None, error)
				else:
					form = SchoolAccommodationTypeForm(instance=queryset)

				template_name = 'admin/master/accommodationtype/edit_school_accommodation_type.html'
				kwvars = {
					'accommodation_type':queryset,
					'form': form,
				}
				
				return render(request, template_name, kwvars)	
			else:
				permission = "permission"
				return render(request, 'admin/master/accommodationtype/edit_school_accommodation_type.html', {'permission': permission})
		except School.DoesNotExist:
			permission = "permission"
			return render(request, 'admin/master/accommodationtype/edit_school_accommodation_type.html', {'permission': permission})
	else:
		permission = "permission"
		return render(request, 'admin/master/accommodationtype/edit_school_accommodation_type.html', {'permission': permission})


@login_required
def delete_school_accommodation_type(request, pk):
	user=request.user
	if user.groups.filter(name='school').exists():
		logged_in_user = request.user.organizationuserprofile.ref_school.id
		print(logged_in_user)
		try:
			accommodationtype = SchoolAccommodationType.objects.get(id=pk)
			_id=accommodationtype.ref_school.id
			
			if logged_in_user==_id:
				if request.method == 'POST':
					accommodationtype.delete()
					print("Delete Successfully")
					return redirect('web:deatil_school', pk=accommodationtype.ref_school.id)
				else:
					pass
				return render(request, 'admin/master/accommodationtype/delete_school_accommodation_type.html', {'accommodationtype': accommodationtype})
			else:
				print("==============================auth error===========")
				permission = "permission"
				return render(request, 'admin/address/accommodationtype/delete_school_accommodation_type.html', {'permission': permission})

		except:
			print("==============================try error===========")
			permission = "permission"
			return render(request, 'admin/master/accommodationtype/delete_school_accommodation_type.html', {'permission': permission})

	else:
		print("==============================groups error===========")
		permission = "permission"
		return render(request, 'admin/master/accommodationtype/delete_school_accommodation_type.html', {'permission': permission})

