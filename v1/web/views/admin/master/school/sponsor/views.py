from datetime import date, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from v1.db.master.school import School
from v1.db.school.school_sponsor import SchoolSponsor
from v1.web.utils import CHECK_USER_PERMISSION
from v1.web.views.admin.master.school.sponsor import SchoolSponsorForm
from v1.base.configs import cRequest
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError


class CreateSchoolSponsor(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('db.add_schoolsponsor',)
    model = SchoolSponsor
    form_class = SchoolSponsorForm
    template_name = 'admin/master/sponsor/add.html'

    def __init__(self):
        super().__init__()

    def get(self, request, *args, **kwargs):
        cRequest.params["school_id"] = kwargs.get("pk")
        school_id = kwargs.get("pk")
        school = get_object_or_404(School, pk=school_id)
        CHECK_USER_PERMISSION(self.request, school)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('web:deatil_school', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Add School Sponsor"
        context['school'] = cRequest.params["school_id"]
        cRequest.params["school_id"] = context['school']
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)

        school_id = cRequest.params["school_id"]
        cRequest.params["school_id"] = school_id
        try:
            school = get_object_or_404(School, pk=school_id)
            obj.ref_school = school
            messages.success(self.request, 'Successfully Added.')
            return super(__class__, self).form_valid(form)
        except IntegrityError:
            error = 'Sponsor with this email already exist.'
            form.add_error(None, error)

        return super(__class__, self).form_invalid(form)


class UpdateSchoolSponsor(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('db.change_schoolsponsor',)
    model = SchoolSponsor
    form_class = SchoolSponsorForm
    template_name = 'admin/master/sponsor/add.html'

    def __init__(self):
        super().__init__()

    def get_success_url(self):
        return reverse('web:deatil_school', args=(self.object.ref_school.id,))

    def get_context_data(self, **kwargs):
        CHECK_USER_PERMISSION(self.request, self.object.ref_school)
        context = super().get_context_data(**kwargs)

        context['title'] = 'Update School Sponsor'
        context['school'] = self.object.ref_school.id
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)

        school_id = self.object.ref_school.id
        cRequest.params["school_id"] = school_id
        try:
            school = get_object_or_404(School, pk=school_id)
            obj.ref_school = school
            messages.success(self.request, 'Successfully Added.')
            return super(__class__, self).form_valid(form)
        except IntegrityError:
            error = 'Sponsor with this email already exist.'
            form.add_error(None, error)

        return super(__class__, self).form_invalid(form)


class DeleteSchoolSponsor(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('db.delete_schoolsponsor',)
    model = SchoolSponsor
    template_name = 'admin/master/sponsor/delete.html'
    pk_url_kwarg = 'pk'

    def get_success_url(self):
        return reverse('web:deatil_school', args=(self.object.ref_school.id,))

    def get_context_data(self, **kwargs):
        CHECK_USER_PERMISSION(self.request, self.object.ref_school)
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete School Sponsor'
        context['school'] = self.object.ref_school.id
        context['page'] = 'Delete School Sponsor'
        context['content'] = 'Are you sure you want to delete ?'
        return context
