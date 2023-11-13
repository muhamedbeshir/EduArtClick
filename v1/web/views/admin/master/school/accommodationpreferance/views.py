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
def create_school_accommodation_preferance(request, pk):
	user=request.user
	if user.groups.filter(name='school').exists():
		logged_in_user = request.user.organizationuserprofile.ref_school.id
		try:
			accommodation = SchoolAccommodationService.objects.get(id=pk)
			if logged_in_user == accommodation.ref_school.id:

				accommodation = SchoolAccommodationService.objects.filter(pk=pk)
				accommodation = accommodation.first()
				context = {}
				form = SchoolAccommodationPreferanceForm(request.POST or None)
				data = request.POST.dict()
				if request.method=='POST':
					if form.is_valid():
						name = data.get('name')
						accommodation_preferance = form.save(commit=False)
						accommodation_preferance.ref_accommodation = accommodation
						accommodation_preferance.save()
						return redirect('web:deatil_school', pk=accommodation.ref_school.id)
					else:
						print("Form is not valid")
						error = "Form is not valid"
						#form.add_error(None, error)

				context['accommodation'] = accommodation
				context['form'] = form
				return render(request, 'admin/master/accommodationpreferance/create_school_accommodation_preferance.html', context)
			else:
				permission = "permission"
				return render(request, 'admin/master/accommodationpreferance/create_school_accommodation_preferance.html', {'permission': permission})

		except SchoolAccommodationService.DoesNotExist:
			permission = "permission"
			return render(request, 'admin/master/accommodationpreferance/create_school_accommodation_preferance.html', {'permission': permission})

	else:
		permission = "permission"
		return render(request, 'admin/master/accommodationpreferance/create_school_accommodation_preferance.html', {'permission': permission})


@login_required
def edit_school_accommodation_preferance(request, pk):
	user=request.user
	if user.groups.filter(name='school').exists():
		logged_in_user = request.user.organizationuserprofile.ref_school.id
		try:
			queryset = SchoolAccommodationPreferance.objects.get(id=pk)
			if logged_in_user == queryset.ref_accommodation.ref_school.id:
				data = request.POST.dict()
				form = SchoolAccommodationPreferanceForm(instance=queryset)
				if request.method=='POST':
					form = SchoolAccommodationPreferanceForm(request.POST, instance=queryset)
					if form.is_valid():
						form.save()
						print("Successfully edit data")
						return redirect('web:deatil_school', pk=queryset.ref_accommodation.ref_school.id)
					else:
						print("Form is not valid")
						error = "Form is not valid"
						form.add_error(None, error)
				else:
					form = SchoolAccommodationPreferanceForm(instance=queryset)

				template_name = 'admin/master/accommodationpreferance/edit_school_accommodation_preferance.html'
				kwvars = {
					'accommodation_preferanc':queryset,
					'form': form,
				}
				
				return render(request, template_name, kwvars)	
			else:
				permission = "permission"
				return render(request, 'admin/master/accommodationpreferance/edit_school_accommodation_preferance.html', {'permission': permission})
		except SchoolAccommodationPreferance.DoesNotExist:
			permission = "permission"
			return render(request, 'admin/master/accommodationpreferance/edit_school_accommodation_preferance.html', {'permission': permission})
	else:
		permission = "permission"
		return render(request, 'admin/master/accommodationpreferance/edit_school_accommodation_preferance.html', {'permission': permission})


@login_required
def delete_school_accommodation_preferance(request, pk):
	user=request.user
	if user.groups.filter(name='school').exists():
		logged_in_user = request.user.organizationuserprofile.ref_school.id
		print(logged_in_user)
		try:
			accommodationpreferance = SchoolAccommodationPreferance.objects.get(id=pk)
			_id=accommodationpreferance.ref_accommodation.ref_school.id
			
			if logged_in_user==_id:
				if request.method == 'POST':
					accommodationpreferance.delete()
					print("Delete Successfully")
					return redirect('web:deatil_school', pk=accommodationpreferance.ref_accommodation.ref_school.id)
				else:
					pass
				return render(request, 'admin/master/accommodationpreferance/delete_school_accommodation_preferance.html', {'accommodationpreferance': accommodationpreferance})
			else:
				print("==============================auth error===========")
				permission = "permission"
				return render(request, 'admin/address/accommodationpreferance/delete_school_accommodation_preferance.html', {'permission': permission})

		except:
			print("==============================try error===========")
			permission = "permission"
			return render(request, 'admin/master/accommodationpreferance/delete_school_accommodation_preferance.html', {'permission': permission})

	else:
		print("==============================groups error===========")
		permission = "permission"
		return render(request, 'admin/master/accommodationpreferance/delete_school_accommodation_preferance.html', {'permission': permission})

