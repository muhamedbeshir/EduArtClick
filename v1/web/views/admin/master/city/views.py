from django.shortcuts import render,redirect
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse

from v1.db.models import City

from .forms import *

from django.db import transaction, IntegrityError



class AddCity(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
	permission_required = ('db.add_city')
	form_class = CityForm
	template_name = 'admin/master/add_city.html'

	def __init__(self):
		super().__init__()

	def get_success_url(self):
		return reverse('web:city_list')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = "Add City"
		return context

	def form_valid(self, form):
		messages.success(self.request, 'Successfully Added.')
		return super(AddCity, self).form_valid(form)

class ListCity(LoginRequiredMixin, PermissionRequiredMixin, ListView):
	permission_required = ('db.view_city')
	model = City
	context_object_name = 'cities'
	template_name = 'admin/master/city_list.html'

class DeleteCity(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
	permission_required = ('db.delete_city')
	model = City
	template_name = 'admin/master/delete_city.html'
	pk_url_kwarg = 'pk'

	def __init__(self):
		super().__init__()

	def get_success_url(self):
		return reverse('web:city_list')

	def get_context_data(self, **kwargs):
		city_id = self.kwargs.get('pk', None)
		context = super().get_context_data(**kwargs)
		context['page'] = 'Delete City'
		context['content'] = 'Are you sure you want to delete ?'
		return context

class EditCity(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	permission_required = ('db.change_city')
	model = City
	form_class = CityForm
	template_name = 'admin/master/add_city.html'

	def __init__(self):
		super().__init__()

	def get_success_url(self):
		return reverse('web:city_list')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		context['title'] = 'Edit City'
		#context['event'] = event
		return context

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.user = self.request.user
		messages.success(self.request, 'Successfully Update.')
		return super(EditCity, self).form_valid(form)

