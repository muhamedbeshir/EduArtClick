from django.shortcuts import render,redirect
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse

from v1.db.models import Country, City

from .forms import *

from django.db import transaction, IntegrityError



class AddCountry(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
	permission_required = ('db.add_country')
	form_class = CountryForm
	template_name = 'admin/master/add_country.html'

	def __init__(self):
		super().__init__()

	def get_success_url(self):
		return reverse('web:country_list')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "Add Country"
		return context

	def form_valid(self, form):
		messages.success(self.request, 'Successfully Added.')
		return super(AddCountry, self).form_valid(form)

class ListCountry(LoginRequiredMixin, PermissionRequiredMixin, ListView):
	permission_required = ('db.view_country')
	model = Country
	context_object_name = 'countries'
	template_name = 'admin/master/country_list.html'
	#paginate_by = 10


class DeleteCountry(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
	permission_required = ('db.delete_country')
	model = Country
	template_name = 'admin/master/delete_country.html'
	pk_url_kwarg = 'pk'

	def __init__(self):
		super().__init__()

	def get_success_url(self):
		return reverse('web:country_list')

	def get_context_data(self, **kwargs):
		country_id = self.kwargs.get('pk', None)
		context = super().get_context_data(**kwargs)
		context['page'] = 'Delete Country'
		context['content'] = 'Are you sure you want to delete ?'
		return context


class EditCountry(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	permission_required = ('db.change_country')
	model = Country
	form_class = CountryForm
	template_name = 'admin/master/add_country.html'

	def __init__(self):
		super().__init__()

	def get_success_url(self):
		return reverse('web:country_list')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		context['title'] = 'Edit Country'
		#context['event'] = event
		return context


	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.user = self.request.user
		messages.success(self.request, 'Successfully Update.')
		return super(EditCountry, self).form_valid(form)



