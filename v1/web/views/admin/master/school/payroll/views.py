from datetime import date, timedelta
from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from v1.base.configs import cRequest
from v1.db.master.school import School
from django.db import IntegrityError
from django.utils import timezone

from v1.db.school.school_payroll import SchoolPayroll
from v1.web.utils import CHECK_USER_PERMISSION
from v1.web.views.admin.master.school.payroll.forms import SchoolPayrollForm




current_day = date.today()
previous_day = date.today() - timedelta(days=1)


class SchoolPayrollCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('db.add_schoolpayroll',)
    model = SchoolPayroll
    form_class = SchoolPayrollForm
    template_name = 'admin/school/payroll/add.html'

    def __init__(self):
        super().__init__()

    def get(self, request, *args, **kwargs):
        cRequest.params[ "school_id" ] = kwargs.get( "pk" )
        school_id = kwargs.get( "pk" )
        school = get_object_or_404(School, pk=school_id)
        CHECK_USER_PERMISSION(self.request, school)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('web:deatil_school' , kwargs={ "pk" :cRequest.params[ "school_id" ] })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Add School Payroll"
        context['school'] = cRequest.params[ "school_id" ]
        context['cdate'] = current_day

        return context

    def form_valid(self, form):
        obj = form.save(False)
        
        school_id = cRequest.params[ "school_id" ]
        cRequest.params[ "school_id" ] = school_id
        try:
            school = get_object_or_404(School, pk=school_id)
            obj.ref_school = school
            obj.code = f"PAY{obj.ref_school.id}{timezone.now().strftime('%Y%m%d%H%M%S')}"
            messages.success(self.request, 'Successfully Added.')
            return super(__class__, self).form_valid(form)
        except IntegrityError:
            error = 'School should have unique payroll code.'
            form.add_error(None, error)
        
        return super(__class__, self).form_invalid(form)


class SchoolPayrollEditView(PermissionRequiredMixin, UpdateView):
    permission_required = ('db.change_schoolpayroll',)
    model = SchoolPayroll
    form_class = SchoolPayrollForm
    template_name = 'admin/school/payroll/add.html'

    def __init__(self):
        super().__init__()

    def get_success_url(self):
        return reverse('web:deatil_school', args=(self.object.ref_school.id,))

    def get_context_data(self, **kwargs):
        CHECK_USER_PERMISSION(self.request, self.object.ref_school)
        context = super().get_context_data(**kwargs)
        context['title'] = "Edit School Payroll"
        context['school'] = self.object.ref_school.id
        context['cdate'] = current_day

        return context

    def form_valid(self, form):
        obj = form.save(commit=False)

        school_id = self.object.ref_school.id
        cRequest.params[ "school_id" ] = school_id
        try:   
            school = get_object_or_404(School, pk=school_id)
            obj.ref_school = school
            messages.success(self.request, 'Successfully Added.')
            return super(__class__, self).form_valid(form)
        except IntegrityError:
            error = 'School should have unique expenses code.'
            form.add_error(None, error)
        
        return super(__class__, self).form_invalid(form)


class SchoolPayrollDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('db.delete_schoolpayroll',)
    model = SchoolPayroll
    template_name = 'admin/school/setting/school_setting_delete.html'
    pk_url_kwarg = 'pk'

    def __init__(self):
        super().__init__()

    def get_success_url(self):
        return reverse('web:deatil_school' , kwargs={ "pk" :cRequest.params[ "school_id" ] })

    def get_context_data(self, **kwargs):
        CHECK_USER_PERMISSION(self.request, self.object.ref_school)
        context = super().get_context_data(**kwargs)
        context['page'] = 'Delete School Payroll'
        context['content'] = 'Are you sure you want to delete ?'
        
        cRequest.params[ "school_id" ] = context.get( "object" ).ref_school.id
        return context