from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from v1.db.models import Organization, OrganizationUserProfile, Application

from v1.base.configs import cRequest

from .forms import *

from django.db import transaction, IntegrityError


class AddOrganization(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('db.add_organization')
    form_class = OrganizationForm
    template_name = 'admin/organization/add_organization.html'

    def __init__(self):
        super().__init__()

    def get_success_url(self):
        return reverse('web:list_organization')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Add Organization"
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Successfully Added.')
        return super(AddOrganization, self).form_valid(form)


class EditOrganization(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('db.change_organization')
    model = Organization
    form_class = OrganizationForm
    template_name = 'admin/organization/add_organization.html'

    def __init__(self):
        super().__init__()

    def get_success_url(self):
        return reverse('web:list_organization')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'Edit Organization'
        # context['event'] = event
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        messages.success(self.request, 'Successfully Update.')
        return super(EditOrganization, self).form_valid(form)


class ListOrganization(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('db.view_organization')
    model = Organization
    template_name = 'admin/organization/list_organization.html'
    context_object_name = 'organizations'


class DeleteOrganization(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('db.delete_organization')
    model = Organization
    template_name = 'admin/organization/delete_organization.html'
    pk_url_kwarg = 'pk'

    def __init__(self):
        super().__init__()

    def get_success_url(self):
        return reverse('web:country_list')

    def get_context_data(self, **kwargs):
        country_id = self.kwargs.get('pk', None)
        context = super().get_context_data(**kwargs)
        context['page'] = 'Delete'
        context['content'] = 'Are you sure you want to delete ?'
        return context


@login_required
def organization_school_create_view(request, pk):
    profile = OrganizationUserProfile.objects.filter(pk=pk)
    profile = profile.first()
    logged_in_user = request.user.organizationuserprofile.id
    if logged_in_user == profile.id:
        data = request.POST.dict()
        form = SchoolOrganizationForm(data or None, request.FILES or None)
        if request.method == "POST":
            if form.is_valid():
                school = form.save(commit=False)
                school.ref_organization = profile.ref_organization
                school.save()
                print("Successfully Added==============================")
                return redirect('web:deatil_school', pk=school.id)

            else:
                print("form is not valid =================================")
                return render(request, 'admin/organization/organization_school_create.html', {'orga': profile, 'form': form})
        else:
            pass

        return render(request, 'admin/organization/organization_school_create.html', {'orga': profile, 'form': form})

    else:
        template_name = '404.html'
        title = 404
        kwvars = {'data': title, }
        return render(request, template_name, kwvars)


@login_required
def organization_school_user_list(request, pk):
    profile = OrganizationUserProfile.objects.filter(pk=pk)
    profile = profile.first()
    logged_in_user = request.user.organizationuserprofile.id
    if logged_in_user == profile.id:
        data = OrganizationUserProfile.objects.filter(
            ref_organization=profile.ref_organization, ref_user__groups__name__in=['school'])
        print(data)
        return render(request, 'admin/organization/organization_school_user_list.html', {'orga': profile, 'data': data})

    else:
        # template_name = '404.html'
        # title = 404
        # kwvars = {'data': title, }
        # return render(request, template_name, kwvars)
        raise PermissionDenied()


@login_required
def organization_application_list(request, pk):
    profile = OrganizationUserProfile.objects.filter(pk=pk)
    profile = profile.first()

    logged_in_user = request.user.organizationuserprofile.id
    if logged_in_user == profile.id:
        data = Application.objects.filter(
            ref_organization=profile.ref_organization.id)
        # print(data)
        return render(request, 'admin/organization/organization_application_list.html', {'orga': profile, 'data': data})

    else:
        template_name = '404.html'
        title = 404
        kwvars = {'data': title, }
        return render(request, template_name, kwvars)


@login_required
def school_application_list(request, pk):
    profile = OrganizationUserProfile.objects.filter(pk=pk)
    profile = profile.first()

    logged_in_user = request.user.organizationuserprofile.id
    if logged_in_user == profile.id:
        data = Application.objects.filter(ref_school=profile.ref_school.id)
        print(data)
        return render(request, 'admin/organization/organization_application_list.html', {'orga': profile, 'data': data})

    else:
        template_name = '404.html'
        title = 404
        kwvars = {'data': title, }
        return render(request, template_name, kwvars)
