from datetime import date, timedelta
from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from v1.db.master.school_course import SchoolCourse
from v1.db.school.school_course_discount import SchoolCourseDiscount
from v1.web.utils import CHECK_USER_PERMISSION
from v1.web.views.admin.master.school.discount.forms import SchoolCourseDiscountForm
from v1.base.configs import cRequest
from v1.db.master.school import School
from django.db import IntegrityError


current_day = date.today()
previous_day = date.today() - timedelta(days=1)


class SchoolCourseDiscountCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('db.add_schoolcoursediscount',)
    model = SchoolCourseDiscount
    form_class = SchoolCourseDiscountForm
    template_name = 'admin/school/discount/add_school_course_discount.html'

    def get(self, request, *args, **kwargs):
        course_id = kwargs.get( "pk" )
        self.course = get_object_or_404(SchoolCourse, pk=course_id)
        CHECK_USER_PERMISSION(self.request, self.course.ref_school)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('web:details_school_course' , kwargs={ "pk": self.object.ref_course.pk })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Add Course Discount"
        context['course'] = self.course
        context['cdate'] = current_day

        return context

    def form_valid(self, form):
        obj = form.save(False)
        course_id = self.kwargs.get( "pk" )
        course = get_object_or_404(SchoolCourse, pk=course_id)
        try:
            obj.ref_course = course
            obj.ref_school = course.ref_school
            messages.success(self.request, 'Successfully Added.')
            return super(__class__, self).form_valid(form)
        except IntegrityError:
            error = 'School should have unique coupon code.'
            form.add_error(None, error)
        
        return super(__class__, self).form_invalid(form)


class SchoolCourseDiscountEditView(PermissionRequiredMixin, UpdateView):
    permission_required = ('db.change_schoolcoursediscount',)
    model = SchoolCourseDiscount
    form_class = SchoolCourseDiscountForm
    template_name = 'admin/school/discount/add_school_course_discount.html'

    def get_success_url(self):
        return reverse('web:details_school_course' , kwargs={ "pk": self.object.ref_course.pk })

    def get_context_data(self, **kwargs):
        CHECK_USER_PERMISSION(self.request, self.object.ref_school)
        context = super().get_context_data(**kwargs)
        context['title'] = "Edit Course Discount"
        context['course'] = self.object.ref_course
        context['cdate'] = current_day

        return context

    def form_valid(self, form):
        obj = form.save(commit=False)

        try:
            messages.success(self.request, 'Successfully Added.')
            return super(__class__, self).form_valid(form)
        except IntegrityError:
            error = 'School should have unique coupon code.'
            form.add_error(None, error)
        
        return super(__class__, self).form_invalid(form)


class SchoolCourseDiscountDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('db.delete_schoolcoursediscount',)
    model = SchoolCourseDiscount
    template_name = 'admin/school/discount/delete.html'
    pk_url_kwarg = 'pk'


    def get_success_url(self):
        return reverse('web:details_school_course' , kwargs={ "pk": self.object.ref_course.pk })

    def get_context_data(self, **kwargs):
        CHECK_USER_PERMISSION(self.request, self.object.ref_school)
        context = super().get_context_data(**kwargs)
        context['page'] = 'Delete Course Discount'
        context['content'] = 'Are you sure you want to delete ?'
        
        return context