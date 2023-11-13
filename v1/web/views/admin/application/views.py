import math
import os
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.http import Http404, HttpResponse
from rest_framework.response import Response
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from django.core.mail import EmailMessage, send_mail
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required
from django.template.loader import render_to_string
from v1.base.utils.pdf import PDFRender
from django.template.loader import get_template
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
import json
import datetime
import stripe
from datetime import date, timedelta
from django.utils import timezone
import mimetypes
from v1.db.master.school_class_installment import SchoolClassInstallment
import io
from django.http import FileResponse

from v1.db.models import *
from v1.db.user.student_profile_has_service import StudentProfileHasService
from v1.web.utils import CHECK_USER_PERMISSION

from .forms import *

from .serializers import ApplicationTokenSerializer, ApplicationServiceSerializer

from django.forms import formset_factory
from django.forms import modelformset_factory
from django.db import transaction, IntegrityError

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

current_day = date.today()
previous_day = date.today() - timedelta(days=1)


def calculate_data(s_start_date, study_period, s_accommodation, s_service, s_course, ref_ap_coupon):
    if s_start_date and study_period:
        day = (int(study_period) * 7)-3
        date_1 = datetime.datetime.strptime(s_start_date, "%Y-%m-%d")
        date_2 = date_1 + datetime.timedelta(days=day)
        start_date = date_1.strftime('%Y-%m-%d')
        end_date = date_2.strftime('%Y-%m-%d')

    service = []
    perweek_data = []
    onetime_data = []
    accommodation_data = []
    perweek_total = 0
    onetime_total = 0
    accommodation_total_cost = 0

    # accommodation_title = s_accommodation.accommodation_title
    if s_accommodation:
        accommodation_total_cost = float(
            s_accommodation.price)*int(study_period)
        accommodation_data.append({
            "id": s_accommodation.id,
            "accommodation_title": s_accommodation.accommodation_title,
            "accommodation_unit_price": float(s_accommodation.price),
            "accommodation_total_cost": accommodation_total_cost
        })

    for x in s_service:
        if x.service_type == 1:

            perweek_data.append({
                "p_service_name": x.service_name,
                "p_service_type": x.service_type_title,
                "p_service_unit_price": float(x.price),
                "p_service_price_total": float(x.price)*int(study_period)
            })
            p_service_price_total = float(x.price)*int(study_period)
            perweek_total += float(p_service_price_total)

        elif x.service_type == 2:
            onetime_data.append({
                "service_name": x.service_name,
                "service_type": x.service_type_title,
                "o_service_unit_price": float(x.price),
                "service_price_total": float(x.price)*int(1)
            })
            service_price_total = float(x.price)*int(1)
            onetime_total += float(service_price_total)
    cours = []
    total = 0
    for s_price in s_price:
        price = s_price.price
        total = float(price)*int(study_period)
        cours.append({
            "coures_name": s_course.title,
            "coures_unit_price": float(s_price.price),
            "coures_price_total": total
        })

    total_cost = 0
    total_cost = float(total+accommodation_total_cost +
                       perweek_total+onetime_total)
    service.append({
        "perweek": perweek_data,
        "perweek_total": perweek_total,
        "onetime": onetime_data,
        "onetime_total": onetime_total

    })

    #
    coupon_discount = 0.0
    grand_total_cost = total_cost

    if ref_ap_coupon:
        coupon_discount = (total*float(ref_ap_coupon.discount))/100
        grand_total_cost = total_cost - coupon_discount

    service_tax = 0.0
    grand_total_cost = grand_total_cost + service_tax


@login_required
@permission_required(['db.add_application'], raise_exception=True)
@api_view(('GET', 'POST'))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def course_calculate_cost(request):
    form = CalculateForm(request.POST or None)

    print(form)
    if request.method == "POST":
        s_country = form.cleaned_data['s_country']
        s_city = form.cleaned_data['s_city']
        s_school = form.cleaned_data['s_school']
        s_course = form.cleaned_data['s_course']
        s_level = None  # form.cleaned_data['s_level']
        s_service = form.cleaned_data['s_service']
        s_price = form.cleaned_data['s_price']
        study_period = form.cleaned_data['study_period']
        s_start_date = form.cleaned_data['s_start_date']
        s_accommodation = form.cleaned_data['s_accommodation']
        s_course_class = form.cleaned_data['course_class']
        # ref_ap_coupon
        # print('=>'*10, form.cleaned_data)
        ref_ap_coupon = form.cleaned_data['ref_ap_coupon']

        course_class = get_object_or_404(SchoolClass, pk=s_course_class)

        if s_start_date and study_period:
            day = (int(study_period) * 7)-3
            date_1 = datetime.datetime.strptime(s_start_date, "%Y-%m-%d")
            date_2 = date_1 + datetime.timedelta(days=day)
            start_date = date_1.strftime('%Y-%m-%d')
            end_date = date_2.strftime('%Y-%m-%d')

            print(end_date, course_class.summar_end)

            if course_class.summar_end < date_2.date():
                print("[-] You can't apply for this course because course end date is less than application course end date.")
                form.add_error(None, 'Application end date should be less than course end date.')
                return render(request, 'admin/application/course_calculate_cost.html', {'form': form, 'cdate': current_day, 'pdate': previous_day})


        service = []
        perweek_data = []
        onetime_data = []
        accommodation_data = []
        perweek_total = 0
        onetime_total = 0
        accommodation_total_cost = 0

        # accommodation_title = s_accommodation.accommodation_title
        if s_accommodation:
            accommodation_total_cost = float(
                s_accommodation.price)*int(study_period)
            accommodation_data.append({
                "id": s_accommodation.id,
                "accommodation_title": s_accommodation.accommodation_title,
                "accommodation_unit_price": float(s_accommodation.price),
                "accommodation_total_cost": accommodation_total_cost
            })

        for x in s_service:
            if x.service_type == 1:

                perweek_data.append({
                    "p_service_name": x.service_name,
                    "p_service_type": x.service_type_title,
                    "p_service_unit_price": float(x.price),
                    "p_service_price_total": float(x.price)*int(study_period)
                })
                p_service_price_total = float(x.price)*int(study_period)
                perweek_total += float(p_service_price_total)

            elif x.service_type == 2:
                onetime_data.append({
                    "service_name": x.service_name,
                    "service_type": x.service_type_title,
                    "o_service_unit_price": float(x.price),
                    "service_price_total": float(x.price)*int(1)
                })
                service_price_total = float(x.price)*int(1)
                onetime_total += float(service_price_total)
        cours = []
        total = 0

        for s_price in s_price:
            price = s_price.price
            total = float(price)*int(study_period)
            cours.append({
                "coures_name": s_course.title,
                "coures_unit_price": float(s_price.price),
                "coures_price_total": total
            })

        total_cost = 0
        total_cost = float(total+accommodation_total_cost +
                           perweek_total+onetime_total)
        service.append({
            "perweek": perweek_data,
            "perweek_total": perweek_total,
            "onetime": onetime_data,
            "onetime_total": onetime_total

        })

        #
        coupon_discount = 0.0
        grand_total_cost = total_cost

        if ref_ap_coupon:
            coupon_discount = (total*float(ref_ap_coupon.discount))/100
            grand_total_cost = total_cost - coupon_discount

        service_tax = 0.0
        grand_total_cost = grand_total_cost + service_tax

        # print(service)
        ctx = {
            "country": s_country.country_name,
            "city": s_city.city_name,
            "school": s_school.school_name,
            "school_id": s_school.id,
            "organization_id": s_school.ref_organization.id,
            "school_email": s_school.email,
            "school_currency": s_school.ref_currency.currency_short,
            "study_period": study_period,
            "start_date": start_date,
            "end_date": end_date,
            "cours": cours,
            "course_class": s_course_class,
            "s_level": s_level,
            "accommodation": accommodation_data,
            "service": service,
            "total_cost": total_cost,
            # ref_ap_coupon
            "coupon": ref_ap_coupon,
            "coupon_id": ref_ap_coupon.id if ref_ap_coupon else None,
            "coupon_discount": coupon_discount,
            "grand_total_cost": grand_total_cost,
            "service_tax": service_tax,
            'sponsors': SchoolSponsor.objects.filter(ref_school=s_school)
            # Testing Data
        }
        html_invoice = render_to_string(
            'admin/master/html_invoice.html', {'ctx': ctx})
        ctx['html_invoice'] = html_invoice
        # print(ctx)
        form = ApplicationForm()
        return render(request, 'admin/application/course_calculate_cost_result.html', {'ctx': ctx, 'form': form, 'cdate': current_day, 'pdate': previous_day})
        # return redirect('web:submit_application', {'ctx':ctx})

    else:
        form = CalculateForm()
        return render(request, 'admin/application/course_calculate_cost.html', {'form': form, 'cdate': current_day, 'pdate': previous_day})


@login_required
@permission_required(['db.add_application'], raise_exception=True)
def submit_application(request):
    data = request.POST.dict()
    if request.method == 'POST':

        form = ApplicationForm(data or None, request.FILES or None)
        if form.is_valid():
            application = form.save(commit=False)
            ap_country = data.get('ap_country')
            ap_city = data.get('ap_city')
            ap_school = data.get('ap_school')
            ap_school_email = data.get('ap_school_email')
            ap_course_name = data.get('ap_course_name')
            ap_course_class = data.get('ap_course_class')
            ap_course_price_total = data.get('ap_course_price_total')
            ap_currency = data.get('ap_currency')
            ap_sub_total = data.get('ap_sub_total')
            ap_grand_total = data.get('ap_grand_total')
            ap_study_period = data.get('ap_study_period')
            ap_start_date = data.get('ap_start_date')
            ap_end_date = data.get('ap_end_date')
            ap_first_name = data.get('ap_first_name')
            ap_last_name = data.get('ap_last_name')
            ap_gender = data.get('ap_gender')
            ap_date_of_birth = data.get('ap_date_of_birth')
            ref_ap_nationality = data.get('ref_ap_nationality')
            home_address = data.get('home_address')
            post_code = data.get('post_code')
            ap_email = data.get('ap_email')
            ap_phone = data.get('ap_phone')
            ap_json_data = data.get('ap_json_data')
            html_invoice = data.get('html_invoice')
            ap_service_json_data = data.get('ap_service_json_data')

            org_id = data.get('ref_organization')
            sch_id = data.get('ref_school')
            document_file = data.get('document_file')
            ap_level = data.get('ap_level')
            discount_id = data.get('ref_ap_coupon')
            print('=>'*10, type(discount_id))
            discount_obj = None
            if not discount_id == 'None':
                discount_obj = SchoolCourseDiscount.objects.get(id=discount_id)
            print('=> ', discount_id, discount_obj)

            org_obj = Organization.objects.get(id=org_id)
            sch_obj = School.objects.get(id=sch_id)

            application.ref_ap_coupon = discount_obj
            application.ref_organization = org_obj
            application.ref_school = sch_obj
            application.user = request.user

            application.save()
            srs = request.POST.getlist('s_ser')
            item = {}
            item_list = []
            if srs:
                ApplicationService.objects.bulk_create([ApplicationService(
                    **{'ref_application': application, 'ap_service_name': m, 'created_by_id': 1}) for m in srs])
            for sr in srs:
                print(sr)
                item_list.append(
                    {"ref_application": application, "ap_service_name": sr, 'created_by_id': 1})

                # item_json=json.dumps(item)item_data_serializer = ApplicationServiceSerializer(data=item)

            ctoken = get_random_string(192)
            token_data = {"ref_application": application.id, "token": ctoken}
            token_data_serializer = ApplicationTokenSerializer(data=token_data)
            # print(token_data_serializer)

            if token_data_serializer.is_valid():

                token_data_serializer.save()

                try:
                    ct = token_data_serializer.data["token"]
                    domain = str(request.headers['Host'])
                    protocol = str('http://')
                    link_to = str('/link/application/')
                    token = str(ct)
                    link = protocol+domain+link_to+token
                    message = render_to_string('admin/application/aplication_send_email.html', {
                        "link": link,
                        "ap_code": application.ap_code
                    })
                    subject = 'Applicaton for course "'+application.ap_course_name + \
                        '" (application code- '+application.ap_code+')'
                    to_email = application.ap_school_email
                    send_mail(subject, message, settings.EMAIL_HOST_USER, [
                              to_email], fail_silently=False)
                    print("Mail send")
                except Exception as e:
                    print(e)

                return redirect('web:application_list')
            else:
                print("=====================token not save====================")

        else:
            print("=====================error form is not valid=====================")
            print(form.errors)
            return render(request, 'admin/application/course_calculate_cost_result.html', {'form': form})
    # return render(request, 'admin/application/course_calculate_cost_result.html', {'form': form})


class ApplicationListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('db.view_application',)
    model = Application
    context_object_name = 'applications'
    template_name = 'admin/application/application_lis.html'
    # ordering = ['-id']
    paginate_by = 5

    def get_user_role(self):
        role = None
        try:
            user = self.request.user
            if user.is_superuser:
                role = "admin"
            else:
                roles = user.groups.filter().all()
                for _role in roles:
                    role = _role.name
        except Exception as e:
            pass

        return role

    def get_queryset(self):
        role = self.get_user_role()
        print(role)
        if (role == "aggent"):
            queryset = Application.objects.filter(
                user=self.request.user).order_by("-id")

        elif (role == "student"):
            queryset = Application.objects.filter(
                user=self.request.user).order_by("-id")
        else:
            queryset = Application.objects.all().order_by("-id")
        return queryset


def checking_user_permission(request, object):
    user = request.user # Current User
    if user.is_superuser:
        return

    group = user.groups.first().name # Current User Group
    raise_exception = False
    # For Admin, Staff and Super Admin
    # 
    # For Student
    if group == 'student':
        if not (user == object.user):
            raise_exception = True
    # For Agent
    elif group == 'aggent':
        if not (user.aggentuserprofile.ref_user == object.user):
            raise_exception = True
    # For School
    elif group == 'school':
        if not (user.organizationuserprofile.ref_school == object.ref_school):
            raise_exception = True
    # For Organization
    elif group == 'organization':
        if not (user.organizationuserprofile.ref_organization == object.ref_organization):
            raise_exception = True

    if raise_exception:
        raise PermissionDenied()


class ApplicationDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = ('db.view_application')
    model = Application
    context_object_name = 'application'
    template_name = 'admin/application/application_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ApplicationDetailView, self).get_context_data(**kwargs)

        # Checking User Permission
        checking_user_permission(self.request, self.object)
        CHECK_USER_PERMISSION(self.request, self.object.ref_school)

        course_class_name = '-'

        if self.object.ap_course_class:
            school_class = get_object_or_404(
                SchoolClass, pk=self.object.ap_course_class)
            course_class_name = school_class.title

            # Checking School Class Installments Available or Not
            class_installments = SchoolClassInstallment.objects.filter(
                ref_class=school_class)
            
            installments = []
            study_period = self.object.ap_study_period

            for installment in class_installments:
                add_installment = False
                if (installment.type == 'Per Week' and study_period >= 4):
                    add_installment = True
                elif (installment.type == 'Per Month' and study_period >= 8):
                    add_installment = True
                elif (installment.type == 'Three Times' and study_period >= 12):
                    add_installment = True
                
                if add_installment:
                    installments.append(installment)

            context['installments'] = installments

        context['course_class_name'] = course_class_name
        return context

    def get(self, request, *args, **kwargs):
        if (kwargs.get("action")):
            id = kwargs.get("pk")
            query = Application.objects.filter(id=id)
            if (query.exists()):
                obj = query.get()

                action = kwargs.get("action")
                if obj.ap_status == 0:
                    if (action == "approve"):
                        obj.ap_status = 1
                    elif (action == "renew"):
                        obj.ap_status = 2

                    obj.save()

                    return super().get(request, *args, **kwargs)

                elif obj.ap_status == 2:
                    if (action == "resubmit"):
                        obj.ap_status = 0
                    obj.save()

        return super().get(request, *args, **kwargs)


class DeleteApplication(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('db.delete_application')
    model = Application
    template_name = 'admin/application/delete_application.html'
    pk_url_kwarg = 'pk'

    def __init__(self):
        super().__init__()

    def get_success_url(self):
        return reverse('web:application_list')

    def get_context_data(self, **kwargs):
        checking_user_permission(self.request, self.object)
        CHECK_USER_PERMISSION(self.request, self.object.ref_school)
        country_id = self.kwargs.get('pk', None)
        context = super().get_context_data(**kwargs)
        context['page'] = 'Delete'
        context['content'] = 'Are you sure you want to delete ?'
        return context


class ApplicationAprovelLetter(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('db.change_application')
    model = Application
    form_class = ApplicationAprovelForm
    template_name = 'admin/application/application_aprovel_letter.html'

    def __init__(self):
        super().__init__()

    def get_user(self):
        return self.request.user

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('web:application_detail', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        CHECK_USER_PERMISSION(self.request, self.object.ref_school)
        # If application is pending then user can add approval letter
        # If application is rejected or approved then user can not again add approval letter
        if not self.object.ap_status == 0:
            raise PermissionDenied()
        
        context = super().get_context_data(**kwargs)

        context['title'] = 'Application Approved'

        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.ap_status = 1
        obj.save()
        print("==============================objects++=======================")
        _model = Application.objects.get(id=obj.id)
        upload_file = _model.ap_approved_file.path
        email = EmailMessage(
            'Approvel Letter', 'Please find the approvel letter as attached.', settings.EMAIL_HOST_USER, [obj.ap_email])
        email.attach_file(upload_file)
        email.send()

        return super(__class__, self).form_valid(form)


class ApplicationRejectLetter(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('db.change_application')
    model = Application
    form_class = ApplicationRejectForm
    template_name = 'admin/application/application_reject_letter.html'

    def __init__(self):
        super().__init__()

    def get_user(self):
        return self.request.user

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('web:application_detail', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        CHECK_USER_PERMISSION(self.request, self.object.ref_school)
        # If application is pending then user can add approval letter
        # If application is rejected or approved then user can not again add approval letter
        if not self.object.ap_status == 0:
            raise PermissionDenied()
        
        context = super().get_context_data(**kwargs)

        context['title'] = 'Application Reject Form'
        context['app_id'] = self.kwargs['pk']

        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.ap_status = 3
        obj.save()

        return super(__class__, self).form_valid(form)


def invoice_print_page(request, pk=None):
    application = Application.objects.get(pk=pk)
    pass


class InvoicePrint(LoginRequiredMixin, TemplateView):
    template_name = 'admin/application/application_invoice.html'

    def get_context_data(self, **kwargs):
        id = self.request.GET.get('application')

        context = super(InvoicePrint, self).get_context_data(**kwargs)


class ApplicationSendLinkView(CreateView):

    template_name = 'admin/application/application_send_link.html'
    form_class = ApplicationFormLink

    def get(self, request, *args, **kwargs):
        _token = kwargs['token']
        if _token is not None:
            today = datetime.datetime.now()
            start = today.replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + datetime.timedelta(1)

            _start_date = start.strftime("%Y-%m-%d %H:%M:%S")
            _end_date = end.strftime("%Y-%m-%d %H:%M:%S")

            # created_at__range=(_start_date, _end_date)
            _model = ApplicationToken.objects.filter(
                token=_token)

            for token_in in _model:
                ctoken = token_in.token

            if _model.exists():
                application_detail = Application.objects.filter(
                    id=_model.get().ref_application.id)
                form = self.form_class(initial=self.initial)

                ctx = {
                    "data": application_detail,
                    "token": ctoken,
                    "form": form,
                    "code": _model.get().ref_application.ap_code,
                    "service": _model.get().ref_application.ap_service_json_data
                }
                return render(request, 'admin/application/application_send_link.html', ctx)
            else:
                return render(request, 'admin/application/invalid_token_link.html')

    def post(self, request, *args, **kwargs):
        # data = request.POST.dict()

        if request.method == "POST":
            ap_status = request.POST['ap_status']
            token = request.POST['token']
            if token is not None and ap_status is not None:
                token_model = ApplicationToken.objects.get(token=token)
                token_get_delete = ApplicationToken.objects.filter(token=token)
                if ap_status == "1" and aproval_paper is not None:
                    application = Application.objects.filter(
                        id=token_model.ref_application.id)
                    if application.exists():
                        application_model = application.get()
                        application_model.ap_status = 1
                        application_model.save()
                        try:
                            message = render_to_string('admin/application/aplication_accept_email.html', {
                                "link": "link",
                                "ap_code": application_model.ap_code,
                                "app_first_name": application_model.ap_first_name,
                                "ap_status": application_model.ap_status_title
                            })
                            subject = 'Applicaton for course "'+application_model.ap_course_name + \
                                '" (application code- ' + \
                                application_model.ap_code+')'
                            to_email = application_model.ap_email
                            send_mail(subject, message, settings.EMAIL_HOST_USER, [
                                      to_email], fail_silently=False)
                            print("Mail send")
                        except Exception as e:
                            print(e)
                        token_get_delete.get().delete()
                        return redirect('web:application_send_link_succes_message')

                elif ap_status == "2":
                    application = Application.objects.filter(
                        id=token_model.ref_application.id)
                    if application.exists():
                        application_model = application.get()
                        application_model.ap_status = 2
                        application_model.save()
                        try:
                            message = render_to_string('admin/application/aplication_accept_email.html', {
                                "link": "link",
                                "ap_code": application_model.ap_code,
                                "app_first_name": application_model.ap_first_name,
                                "ap_status": application_model.ap_status_title
                            })
                            subject = 'Applicaton for course "'+application_model.ap_course_name + \
                                '" (application code- ' + \
                                application_model.ap_code+')'
                            to_email = application_model.ap_email
                            send_mail(subject, message, settings.EMAIL_HOST_USER, [
                                      to_email], fail_silently=False)
                            print("Mail send")
                        except Exception as e:
                            print(e)
                        token_get_delete.get().delete()
                        return redirect('web:application_send_link_succes_message')
                else:
                    pass

            else:
                token_model = ApplicationToken.objects.get(token=token)
                token_get_delete = ApplicationToken.objects.filter(token=token)
                application = Application.objects.filter(
                    id=token_model.ref_application.id)
                add_error = "Form is not valid"
                ctx = {
                    "data": application,
                    "token": ctoken
                }
                return render(request, self.template_name, {'data': data, 'token': token, 'error': add_error})


class ApplicationSendLinkSuccesMessage(TemplateView):
    template_name = 'admin/application/application_send_link_succes_message.html'


class GeneratePDF(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('db.view_application')

    def get(self, request, *args, **kwargs):
        html = get_template('admin/application/pdf/aplication_pdf.html')
        _token = kwargs['token']
        _model = ApplicationToken.objects.filter(
            token=_token)
        if _model.exists():
            application_detail = Application.objects.filter(
                id=_model.get().ref_application.id)
            title = "Application"
            ctx = {
                'title': title,
                'application_detail': application_detail,
                "code": _model.get().ref_application.ap_code,
                "first_name": _model.get().ref_application.ap_first_name,
                "last_name": _model.get().ref_application.ap_last_name,
                "gender": _model.get().ref_application.ap_gender,
                "date_of_birth": _model.get().ref_application.ap_date_of_birth,
                "home_address": _model.get().ref_application.home_address,
                "post_code": _model.get().ref_application.post_code,
                "nationality": _model.get().ref_application.ref_ap_nationality,
                "ap_email": _model.get().ref_application.ap_email,
                "phone": _model.get().ref_application.ap_phone,
                "first_language": _model.get().ref_application.first_language,
                "religion": _model.get().ref_application.ap_religion,
                "passport_number": _model.get().ref_application.ap_passport_number,
                "passport_expiry_date": _model.get().ref_application.ap_passport_expiry_date
            }
            html = html.render(ctx)
            options = {
                'page-size': 'A4',
            }
            t_model = _model.get()
            no = t_model.ref_application.ap_code
            file = no+'.pdf'
            # return Response(ctx)
            return PDFRender.render(html, file_name=file, **options)


class DownloadApplicationPDF(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('db.view_application')

    def get(self, request, *args, **kwargs):
        html = get_template(
            'admin/application/pdf/download_aplication_pdf.html')
        _id = kwargs['pk']
        _model = Application.objects.filter(
            id=_id)
        print(_model)
        if _model.exists():
            application_detail = _model.get()
            
            CHECK_USER_PERMISSION(self.request, application_detail.ref_school)

            title = "Application"
            ctx = {
                'title': title,
                'detail': _model,
                'ap_code': application_detail.ap_code,
                'first_name': application_detail.ap_first_name,
                'last_name': application_detail.ap_last_name,
                'gender': application_detail.ap_gender,
                'date_of_birth': application_detail.ap_date_of_birth,
                'home_address': application_detail.home_address,
                'post_code': application_detail.post_code,
                'nationality': application_detail.ref_ap_nationality,
                'ap_email': application_detail.ap_email,
                'phone': application_detail.ap_phone,
                'first_language': application_detail.first_language,
                'religion': application_detail.ap_religion,
                'passport_number': application_detail.ap_passport_number,
                'passport_expiry_date': application_detail.ap_passport_expiry_date,
                'ap_course_name': application_detail.ap_course_name,
                'ap_level': application_detail.ap_level,
                'ap_study_period': application_detail.ap_study_period,
                'ap_start_date': application_detail.ap_start_date,
                'ap_end_date': application_detail.ap_end_date

            }
            html = html.render(ctx)
            options = {
                'page-size': 'A4',
            }

            no = application_detail.ap_code
            file = no+'.pdf'

            return PDFRender.render(html, file_name=file, **options)


class DownloadTransactionPDF(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('db.view_application')

    def get(self, request, *args, **kwargs):
        html = get_template(
            'admin/transaction/pdf/download_transaction_pdf.html')
        _id = kwargs['pk']
        _model = Application.objects.filter(id=_id)
        print(_model)
        if _model.exists():
            application_detail = _model.get()
            transaction = Transaction.objects.filter(
                application=application_detail)
            transaction = transaction.first()

            ctx = {
                'ap_code': application_detail.ap_code,
                'ap_course_name': application_detail.ap_course_name,
                'school_name': application_detail.ap_school,
                'total_price': application_detail.ap_grand_total,
                'currency': application_detail.ap_currency,
                'transaction_id': transaction.payment_id,
                'created_at': transaction.created_at,
                'invoice': application_detail.html_invoice,
            }
            html = html.render(ctx)
            options = {
                'page-size': 'A4',
            }

            no = application_detail.ap_code
            file = no+'_TRANSACTION.pdf'

            return PDFRender.render(html, file_name=file, **options)


class DownloadApprovedLetter(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('db.view_application',)
    
    def get(self, request, *args, **kwargs):
        _id = kwargs['pk']
        _model = Application.objects.filter(id=_id)
        if _model.exists():
            application_detail = _model.get()
            CHECK_USER_PERMISSION(self.request, application_detail.ref_school)

            approved_letter = application_detail.ap_approved_file.path
            
            # if file not exist in storage
            if not os.path.exists(approved_letter):
                raise Http404
            
            print("Approved_letter", approved_letter)
            # Open the file for reading content
            path = open(approved_letter, 'rb')
            # Set the mime type
            mime_type, _ = mimetypes.guess_type(approved_letter)
            # Set the return value of the HttpResponse
            response = HttpResponse(path, content_type=mime_type)
            # Set the HTTP header for sending to browser
            response['Content-Disposition'] = f"attachment; filename=APP-00{_id}_APPROVED_LETTER.pdf"
            # Return the response value
            return response


class DownloadPaymentInvoice(LoginRequiredMixin, View):
    # permission_required = ('db.view_application',)
    template_name = 'admin/payment/payment_invoice.html'
    
    def get(self, request, *args, **kwargs):
        student_course_id = self.kwargs.get('course')
        installment_id = self.kwargs.get('ins')

        student_course = get_object_or_404(StudentProfileHasCourse, pk=student_course_id)
        installment = student_course.installments[installment_id - 1]

        CHECK_USER_PERMISSION(request, student_course.ref_course.ref_school)

        if not installment or installment['status'] == "Pending":
            raise Http404

        context = {
            'student': student_course.ref_student,
            'school': student_course.ref_course.ref_school,
            'class': student_course.ref_course,
            'installment': installment,
        }

        response = render(request=request, template_name=self.template_name, context=context)

        # response = HttpResponse(html_string)

        return response



'''
STRIPE PAYMENT INTEGRATION
'''


@login_required
def payment_success(request):
    template_name = 'admin/payment/success.html'

    # print('='*10, request.GET['application_id'], '='*10)
    application_id = request.GET['application']
    if application_id:
        application = get_object_or_404(Application, pk=application_id)

        application_code = application.ap_code
        school = application.ap_school
        course = application.ap_course_name
        payment_currency = str(application.ap_currency)
        payment_amount = int(application.ap_grand_total)

    context = {
        'application_id': application_id,
        'application_code': application_code,
        'school': school,
        'course': course,
        'currency': payment_currency,
        'amount': payment_amount
    }

    return render(request=request, template_name=template_name, context=context)


@login_required
def payment_cancel(request):
    template_name = 'admin/payment/cancel.html'

    # print('='*10, request.GET['application_id'], '='*10)
    application_id = request.GET['application']
    if application_id:
        application = get_object_or_404(Application, pk=application_id)

        # Checking application payment success status or not
        if application.ap_payment_status:
            return redirect('web:application_list')

        application_code = application.ap_code
        school = application.ap_school
        course = application.ap_course_name
        payment_currency = str(application.ap_currency)
        payment_amount = int(application.ap_grand_total)

    context = {
        'application_id': application_id,
        'application_code': application_code,
        'school': school,
        'course': course,
        'currency': payment_currency,
        'amount': payment_amount,
        'transaction_id': '',
    }

    return render(request=request, template_name=template_name, context=context)


@login_required
@csrf_exempt
def create_payment_session(request):
    if request.method == 'POST':
        stripe.api_key = settings.STRIPE_SECRET_KEY
        content = json.loads(request.body.decode('utf-8'))
        application_id = content.get('application_id')
        payment_type = content.get('payment_type')
        installment_type = content.get('installment_type')

        application = get_object_or_404(Application, pk=application_id)

        if payment_type == 'Full Payment' or not (payment_type and installment_type):
            payment_amount = int(application.ap_grand_total)
        elif payment_type == 'In Installments':
            installment = get_object_or_404(SchoolClassInstallment,
                                            ref_class__pk=application.ap_course_class, type=installment_type)

            net_amount = application.ap_grand_total + \
                (application.ap_grand_total * installment.charges) / 100

            divided_by = 0
            if installment_type == 'Per Week':
                divided_by = 1
            elif installment_type == 'Per Month':
                divided_by = 4
            elif installment_type == 'Three Times':
                divided_by = int(application.ap_study_period/3)

            total_installments = int(application.ap_study_period / divided_by)
            payment_amount = round(net_amount / total_installments, 2)
            payment_amount = math.ceil(payment_amount)

        payment_currency = str(application.ap_currency)
        stripe_payment_amount = payment_amount * 100
        customer_email = application.ap_email

        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=request.build_absolute_uri(
                    reverse('web:application_payment_success')) + f'?application={application_id}',
                cancel_url=request.build_absolute_uri(
                    reverse('web:application_payment_cancel')) + f'?application={application_id}',

                client_reference_id=request.user.id if request.user.is_authenticated else None,

                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'price_data': {
                            'currency': payment_currency,
                            'product_data': {
                                'name': 'Teachia Payment Request',
                            },
                            'unit_amount': stripe_payment_amount,
                        },
                        'quantity': 1,
                    },
                ],
                customer_email=customer_email,
                # Update - passing application id in checkout to update the application object in webhook
                metadata={
                    "application_id": application.id,
                    "user_id": request.user.id,
                    "payment_type": payment_type,
                    "installment_type": installment_type
                },
            )
            # print(checkout_session)
            return JsonResponse({
                'session_id': checkout_session.id,
                'stripe_public_key': settings.STRIPE_PUBLISHABLE_KEY,
            })
        except Exception as e:
            print(JsonResponse({'error': str(e)}))
            return JsonResponse({'error': str(e)})


@csrf_exempt
def webhook(request):
    print('='*10, 'Webhook', '='*10)
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        # NEW CODE
        session = event['data']['object']
        sessionID = session["id"]
        # getting information of order from session
        payment_id = session["payment_intent"]
        customer_name = session["customer_details"]["name"]
        customer_email = session["customer_details"]["email"]
        currency = session["currency"]
        amount = session["amount_total"] / 100

        print(session["metadata"])

        if session["metadata"].get("application_id"):
            # grabbing id of the order created
            application_id = session["metadata"]["application_id"]
            user_id = session["metadata"]["user_id"]

            payment_type = session["metadata"]["payment_type"]
            installment_type = session["metadata"]["installment_type"]

            # Updating application payment status
            application = get_object_or_404(Application, id=application_id)
            # Checking Payment Type
            if payment_type == 'Full Payment':
                application.ap_payment_status = 1
            elif payment_type == 'In Installments':
                installment = get_object_or_404(SchoolClassInstallment,
                                                ref_class__pk=application.ap_course_class, type=installment_type)

                net_amount = application.ap_grand_total + \
                    (application.ap_grand_total * installment.charges) / 100

                divided_by = 0
                payment_after = 0
                if installment_type == 'Per Week':
                    divided_by = 1
                    payment_after = 7
                elif installment_type == 'Per Month':
                    divided_by = 4
                    payment_after = 30
                elif installment_type == 'Three Times':
                    divided_by = int(application.ap_study_period / 3)
                    payment_after = 10

                total_installments = int(
                    application.ap_study_period / divided_by)
                installments_amount = round(net_amount / total_installments, 2)

                installments = []
                installment_date = timezone.now().date()

                for idx in range(1, total_installments+1):
                    data_dict = {
                        'id': idx,
                        'type': installment_type,
                        'currency': currency,
                        'amount': amount,
                        'date': str(installment_date),
                        'status': 'Pending',
                        'paid': '-',
                        'transaction': '',
                    }
                    installments.append(data_dict)

                    installment_date = installment_date + \
                        timedelta(days=payment_after)

                # Update 1st Installment Payment Status Done
                installments[0]['status'] = 'Done'
                installments[0]['paid'] = str(timezone.now().date())
                installments[0]['transaction'] = payment_id

                application.installment_sub_total = net_amount
                application.ap_payment_status = 2
                application.payment_in_installment = True
                application.installments = installments

            application.save()

            # Insert Record In Transaction Table
            Transaction.objects.create(
                payment_id=payment_id,
                customer_name=customer_name,
                customer_email=customer_email,
                currency=currency,
                amount=amount,
                status=1,
                application_id=application_id,
                created_by_id=user_id,
                user_id=user_id
            )

        if session["metadata"].get("service_id"):
            # grabbing id of the order created
            service_id = session["metadata"]["service_id"]
            user_id = session["metadata"]["user_id"]

            # Updating user service payment status
            student_service = get_object_or_404(
                StudentProfileHasService, pk=service_id, ref_student__ref_user__pk=user_id)
            student_service.payment = True
            student_service.save()

            # Insert Record In Transaction Table
            Transaction.objects.create(
                payment_id=payment_id,
                customer_name=customer_name,
                customer_email=customer_email,
                currency=currency,
                amount=amount,
                status=1,
                ref_school_service=student_service,
                created_by_id=user_id,
                user_id=user_id
            )

        if session["metadata"].get("accommodation_id"):
            # grabbing id of the order created
            accommodation_id = session["metadata"]["accommodation_id"]
            user_id = session["metadata"]["user_id"]

            # Updating user accommodation payment status
            student_accommodation = get_object_or_404(
                StudentProfileHasAccommodation, pk=accommodation_id, ref_student__ref_user__pk=user_id)
            student_accommodation.payment = True
            student_accommodation.save()

            # Insert Record In Transaction Table
            Transaction.objects.create(
                payment_id=payment_id,
                customer_name=customer_name,
                customer_email=customer_email,
                currency=currency,
                amount=amount,
                status=1,
                ref_school_accommodation_service=student_accommodation,
                created_by_id=user_id,
                user_id=user_id
            )

        if session["metadata"].get("installment_id") and session["metadata"].get("class_id"):
            # grabbing id of the order created
            user_id = session["metadata"]["user_id"]
            installment_id = int(session["metadata"]["installment_id"])
            class_id = int(session["metadata"]["class_id"])
            full_payment = session["metadata"]["full_payment"]

            student_has_course = get_object_or_404(
                StudentProfileHasCourse, pk=class_id)

            if full_payment == "True":
                for installment in student_has_course.installments:
                    if installment['status'] == 'Pending':
                        installment['status'] = 'Done'
                        installment['paid'] = str(timezone.now().date())
                        installment['transaction'] = payment_id
                        student_has_course.save()
            else:
                student_has_course.installments[installment_id - 1]['status'] = 'Done'
                student_has_course.installments[installment_id - 1]['paid'] = str(timezone.now().date())
                student_has_course.installments[installment_id - 1]['transaction'] = payment_id
                student_has_course.save()
                

            # Insert Record In Transaction Table
            Transaction.objects.create(
                payment_id=payment_id,
                customer_name=customer_name,
                customer_email=customer_email,
                currency=currency,
                amount=amount,
                status=1,
                created_by_id=user_id,
                user_id=user_id
            )

        # print(session)

        # print('='*10,
        #       f'Transaction: {payment_id} <=>User: {user_id} <=> Name: {customer_name} <=> Email: {customer_email} <=> Currency: {currency} <=> Amount: {amount} <=> Session Id: {sessionID}',
        #       '='*10)
        return HttpResponse(status=200)
