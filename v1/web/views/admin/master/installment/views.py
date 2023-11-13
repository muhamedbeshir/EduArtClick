from typing import Any
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib import messages
from v1.db.master.school_class import SchoolClass
from v1.db.master.school_class_installment import SchoolClassInstallment
from v1.web.utils import CHECK_USER_PERMISSION
from .forms import SchoolClassInstallmentForm


class CreateSchoolClassInstallment(PermissionRequiredMixin, CreateView):
    permission_required = ('db.add_schoolclassinstallment',)
    template_name = 'admin/master/installment/add.html'
    model = SchoolClassInstallment
    form_class = SchoolClassInstallmentForm

    def get_success_url(self) -> str:
        return reverse_lazy('web:detail_school_course', kwargs={'pk': self.object.ref_class.pk})

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add School Class Installment'
        context['class_id'] = self.kwargs.get('pk')
        class_id = self.kwargs.get('pk')
        school_class = get_object_or_404(SchoolClass, pk=class_id)
        CHECK_USER_PERMISSION(self.request, school_class.ref_school)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        class_id = context['class_id']

        obj = form.save(commit=False)

        try:
            # Assign SchoolClass object obj.ref_class
            obj.ref_class = get_object_or_404(SchoolClass, pk=class_id)
            obj.save()
            msg = f'Class Installment "{obj.type}" added successfully.'
            print(f'[+] {msg}')
            messages.success(self.request, msg)
        except IntegrityError:
            msg = f'Class Installment "{obj.type}" already exists.'
            form.add_error('', msg)
            return super().form_invalid(form)

        return super().form_valid(form)


class UpdateSchoolClassInstallment(PermissionRequiredMixin, UpdateView):
    permission_required = ('db.change_schoolclassinstallment',)
    template_name = 'admin/master/installment/add.html'
    model = SchoolClassInstallment
    form_class = SchoolClassInstallmentForm

    def get_success_url(self) -> str:
        return reverse_lazy('web:detail_school_course', kwargs={'pk': self.object.ref_class.pk})

    def get_context_data(self, **kwargs: Any):
        CHECK_USER_PERMISSION(self.request, self.object.ref_class.ref_school)
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update School Class Installment'
        context['class_id'] = self.object.ref_class.pk
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        try:
            obj.save()
            msg = f'Class Installment "{obj.type}" updated successfully.'
            print(f'[+] {msg}')
            messages.success(self.request, msg)
        except IntegrityError:
            msg = f'Class Installment "{obj.type}" already exists.'
            form.add_error('', msg)
            return super().form_invalid(form)

        return super().form_valid(form)


class DeleteSchoolClassInstallment(PermissionRequiredMixin, DeleteView):
    permission_required = ('db.delete_schoolclassinstallment',)
    template_name = 'admin/master/delete_city.html'
    model = SchoolClassInstallment
    pk_url_kwarg = 'pk'

    def get_success_url(self) -> str:
        return reverse_lazy('web:detail_school_course', kwargs={'pk': self.object.ref_class.pk})

    def get_context_data(self, **kwargs):
        CHECK_USER_PERMISSION(self.request, self.object.ref_class.ref_school)
        context = super().get_context_data(**kwargs)
        context['page'] = 'Delete School Class Installment'
        context['content'] = 'Are you sure you want to delete ?'
        return context
