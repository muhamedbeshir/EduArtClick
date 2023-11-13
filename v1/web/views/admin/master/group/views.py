from typing import Any, Dict
from django.shortcuts import render,redirect
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group, Permission
from django.db import transaction, IntegrityError
from .forms import *



class ListGroup(LoginRequiredMixin, PermissionRequiredMixin, ListView):
	permission_required = ('auth:view_group')
	model = Group
	context_object_name = 'groups'
	template_name = 'admin/master/group/list.html'
	#paginate_by = 10

	def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
		context = super().get_context_data(**kwargs)
		return context

# Create a group which hold the permission
class AddGroup(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
	template_name = 'admin/master/group/add.html'
	permission_required = ('auth:add_group',)
	model = Group
	form_class = GroupForm

	def get_success_url(self) -> str:
		return reverse('web:list_group')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Add Group'
		content_types = ContentType.objects.all().exclude(id__in = (1,2,3,4,5,6,7,8,9,10,11,12)).order_by('pk').prefetch_related('permission_set')
		context['content_types'] = content_types

		return context

	def form_valid(self, form):
		group_permissions = self.request.POST.getlist("permissions")
		print(group_permissions)
		with transaction.atomic():
			obj = form.save(commit=False)
			print(obj)
			permissions = Permission.objects.filter(id__in=group_permissions)
			obj.save()
			obj.permissions.set(permissions)

			msg = f'Group "{self.object}" added successfully.'
			print(f'[+] {msg}')
			messages.success(self.request, msg)

		return super().form_valid(form)


# Update a group which hold the permission
class UpdateGroup(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	template_name = 'admin/master/group/add.html'
	permission_required = ('auth:change_group',)
	model = Group
	form_class = GroupForm

	def get_success_url(self) -> str:
		return reverse('web:list_group')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		# permissions = Permission.objects.all().exclude(content_type_id__in = (1,2,3,4,5,6,7,8,9,10,11,12)).order_by('content_type_id').select_related('content_type')
		# context['permissions'] = permissions.exclude(pk__in=(cperm.pk for cperm in current_permissions))
		# print(current_permissions)
		
		current_permissions = self.object.permissions.all().order_by('content_type_id')
		content_types = ContentType.objects.all().exclude(id__in = (1,2,3,4,5,6,7,8,9,10,11,12)).order_by('pk').prefetch_related('permission_set')

		context['title'] = 'Update Group'
		context['content_types'] = content_types
		context['current_permissions'] = current_permissions

		return context

	def form_valid(self, form):
		group_permissions = self.request.POST.getlist('permissions')

		with transaction.atomic():
			obj = form.save(commit=False)
			permissions = Permission.objects.filter(id__in=group_permissions)
			obj.save()
			obj.permissions.set(permissions)
			
			msg = f'Group "{self.object}" updated successfully.'
			print(f'[+] {msg}')
			messages.success(self.request, msg)

		return super().form_valid(form)
    


class DeleteGroup(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
	template_name = 'admin/master/group/delete.html'
	permission_required = ('auth.delete_group')
	model = Group
	context_object_name = 'group'
	pk_url_kwarg = 'pk'

	def get_success_url(self) -> str:
		return reverse('web:list_group')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Delete Group'
		context['content'] = 'Are you sure you want to delete ?'
		return context

	def form_valid(self, form):
		msg = 'Group "{self.object}" deleted successfully.'
		print(f'[+] {msg}')
		messages.success(self.request, msg)
		return super().form_valid(form)

# class DeleteCountry(LoginRequiredMixin, DeleteView):
#     model = Country
#     template_name = 'admin/master/delete_country.html'
#     pk_url_kwarg = 'pk'

#     def __init__(self):
#         super().__init__()

#     def get_success_url(self):
#         return reverse('web:country_list')

#     def get_context_data(self, **kwargs):
#     	country_id = self.kwargs.get('pk', None)
#     	context = super().get_context_data(**kwargs)
#     	context['page'] = 'Delete Country'
#     	context['content'] = 'Are you sure you want to delete ?'
#     	return context

# class EditCountry(LoginRequiredMixin, UpdateView):
# 	model = Country
# 	form_class = CountryForm
# 	template_name = 'admin/master/add_country.html'

# 	def __init__(self):
# 		super().__init__()

# 	def get_success_url(self):
# 		return reverse('web:country_list')

# 	def get_context_data(self, **kwargs):
# 		context = super().get_context_data(**kwargs)
		
# 		context['title'] = 'Edit Country'
# 		#context['event'] = event
# 		return context


# 	def form_valid(self, form):
# 		obj = form.save(commit=False)
# 		obj.user = self.request.user
# 		messages.success(self.request, 'Successfully Update.')
# 		return super(EditCountry, self).form_valid(form)



