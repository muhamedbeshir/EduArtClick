from datetime import date, timedelta
from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from v1.base.configs import cRequest
from v1.db.master.school import School
from django.db import IntegrityError

from v1.db.school.school_expense import SchoolExpense
from v1.web.utils import CHECK_USER_PERMISSION
from v1.web.views.admin.master.school.expenses.forms import SchoolExpensesForm


current_day = date.today()
previous_day = date.today() - timedelta(days=1)


class SchoolExpenseCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('db.add_schoolexpense',)
    model = SchoolExpense
    form_class = SchoolExpensesForm
    template_name = 'admin/school/expense/add_school_expense.html'

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
        context['title'] = "Add School Expense"
        context['school'] = cRequest.params[ "school_id" ]
        context['cdate'] = current_day

        return context

    def form_valid(self, form):
        obj = form.save(False)
        
        school_id = cRequest.params[ "school_id" ]
        cRequest.params[ "school_id" ] = school_id
        try:
            if obj.expense_type == 'External':
                obj.internal_expense_type = None

            school = get_object_or_404(School, pk=school_id)
            obj.ref_school = school
            messages.success(self.request, 'Successfully Added.')
            return super(__class__, self).form_valid(form)
        except IntegrityError:
            error = 'School should have unique expenses name.'
            form.add_error(None, error)
        
        return super(__class__, self).form_invalid(form)

class SchoolExpenseEditView(PermissionRequiredMixin, UpdateView):
    permission_required = ('db.change_schoolexpense',)
    model = SchoolExpense
    form_class = SchoolExpensesForm
    template_name = 'admin/school/expense/add_school_expense.html'

    def __init__(self):
        super().__init__()

    def get_success_url(self):
        return reverse('web:deatil_school', args=(self.object.ref_school.id,))

    def get_context_data(self, **kwargs):
        CHECK_USER_PERMISSION(self.request, self.object.ref_school)
        context = super().get_context_data(**kwargs)
        context['title'] = "Edit School Expense"
        context['school'] = self.object.ref_school.id
        context['cdate'] = current_day

        return context

    def form_valid(self, form):
        obj = form.save(commit=False)

        school_id = self.object.ref_school.id
        cRequest.params[ "school_id" ] = school_id
        try:
            if obj.expense_type == 'External':
                obj.internal_expense_type = None
                
            school = get_object_or_404(School, pk=school_id)
            obj.ref_school = school
            messages.success(self.request, 'Successfully Added.')
            return super(__class__, self).form_valid(form)
        except IntegrityError:
            error = 'School should have unique expenses name.'
            form.add_error(None, error)
        
        return super(__class__, self).form_invalid(form)


class SchoolExpenseDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('db.delete_schoolexpense',)
    model = SchoolExpense
    template_name = 'admin/school/setting/school_setting_delete.html'
    pk_url_kwarg = 'pk'

    def __init__(self):
        super().__init__()

    def get_success_url(self):
        return reverse('web:deatil_school' , kwargs={ "pk" :cRequest.params[ "school_id" ] })

    def get_context_data(self, **kwargs):
        CHECK_USER_PERMISSION(self.request, self.object.ref_school)
        context = super().get_context_data(**kwargs)
        context['page'] = 'Delete School Expense'
        context['content'] = 'Are you sure you want to delete ?'
        
        cRequest.params[ "school_id" ] = context.get( "object" ).ref_school.id
        return context