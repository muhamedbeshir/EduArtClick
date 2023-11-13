from datetime import date, timedelta, datetime
from decimal import Decimal
from django.contrib.auth.models import User
import json
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models.functions import ExtractYear, ExtractMonth
import stripe
from v1.db.models import *
import calendar
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Sum, F
from v1.base.configs import cRequest
from v1.db.user.student_profile_has_service import StudentProfileHasService

# Create your views here.
current_day = date.today()


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = "admin/dashboard.html"

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

    def aplication_get_data(self):
        user = self.request.user
        role = self.get_user_role()

        # print('='*20, user, role)
        print(role)
        if (role == "aggent"):
            ap_status = Application.objects.filter(user=user).values(
                'ap_status').annotate(Count('ap_status'))
        elif (role == "student"):
            ap_status = Application.objects.filter(user=user).values(
                'ap_status').annotate(Count('ap_status'))
        elif (role == "organization"):
            org_user = OrganizationUserProfile.objects.get(ref_user=user)
            ap_status = Application.objects.filter(ref_organization=org_user.ref_organization.id).values(
                'ap_status').annotate(Count('ap_status'))
        elif (role == "school"):
            school_user = OrganizationUserProfile.objects.get(ref_user=user)
            print(school_user.ref_school)
            ap_status = Application.objects.filter(ref_school=school_user.ref_school.id).values(
                'ap_status').annotate(Count('ap_status'))
        elif (role == "staff"):
            ap_status = Application.objects.values(
                'ap_status').annotate(Count('ap_status'))
        else:
            ap_status = Application.objects.values(
                'ap_status').annotate(Count('ap_status'))

        if ap_status:
            level = []
            for x in ap_status:
                print(x)
                if x.get('ap_status') == 0:
                    level.append('Pending')
                elif x.get('ap_status') == 1:
                    level.append('Accepted')
                elif x.get('ap_status') == 2:
                    level.append('Renew')
                elif x.get('ap_status') == 3:
                    level.append('Rejected')

            value = [y.get('ap_status__count') for y in ap_status]

            context = {
                'ap_status': ap_status,
                'level': level,
                'value': value,
            }
            # print(context)
            # return context
        else:
            context = {
                'ap_status': ap_status,
                'level': ['Pending', 'Accepted', 'Rejected'],
                'value': ['0', '0', '0'],
            }
        # print(context)
        return context

    def aplication_get_data_by_year(self):
        ap = Application.objects.values('year').annotate(Count('year'))

        level = []
        for x in ap:
            pass
        context = {
            'year': ap
        }
        return context

    def expenses_get_data(self):
        user = self.request.user
        role = self.get_user_role()

        if (role == "school"):
            school_user = OrganizationUserProfile.objects.get(ref_user=user)
            print(school_user.ref_school)
            ###### Track School Expenses #####
            school_expenses = SchoolExpense.objects.filter(ref_school=school_user.ref_school.id).annotate(
                year=ExtractYear(F('created_at')),
                month=ExtractMonth(F('created_at')),
            )
            school_earnings = Application.objects.filter(ref_school=school_user.ref_school.id).annotate(
                month=ExtractMonth(F('created_at')),
            )

            s_expenses = school_expenses.values('year', 'month').annotate(
                sum_amount=Sum('amount')).order_by('-year', '-month')
            s_earnings = school_earnings.values('year', 'month').annotate(sum_amount=Sum(
                'ap_grand_total'), sum_discount=Sum('ap_course_discount')).order_by('-year', '-month')
            print('[*] School Expenses :: ', s_expenses)
            print('\n[*] School Earnings :: ', s_earnings)

            s_course_expenses = school_expenses.values('year', 'month', 'ref_school_course').annotate(
                sum_amount=Sum('amount')).order_by('-year', '-month')
            s_course_earnings = school_earnings.values('year', 'month', 'ap_course_name').annotate(
                sum_amount=Sum('ap_course_price_total')).order_by('-year', '-month')
            s_service_expenses = school_expenses.values('year', 'month', 'ref_school_service').annotate(
                sum_amount=Sum('amount')).order_by('-year', '-month')
            # s_teacher_expenses = school_expenses.values('year', 'month', 'ref_school_teacher').annotate(sum_amount=Sum('amount')).order_by('-year', '-month')
            # s_other_expenses = school_expenses.values('year', 'month', 'internal_expense_type').annotate(sum_amount=Sum('amount')).order_by('-year', '-month')

            print('\n[*] School Course Expenses :: ', s_course_expenses)
            print('\n[*] School Course Earnings :: ', s_course_earnings)
            print('\n[*] School Service Expenses :: ', s_service_expenses)
            # print('\n[*] School Teacher Expenses :: ', s_teacher_expenses)
            # print('\n[*] School Other Expenses :: ', s_other_expenses)

            year_wise_data = {
                # "2023": {"months": [], "earnings": [], "expenses": []}
            }

            months_list = ['Dec', 'Nov', 'Oct', 'Sep', 'Aug',
                           'Jul', 'Jun', 'May', 'Apr', 'Mar', 'Feb', 'Jan']
            amount_list = ['0.0', '0.0', '0.0', '0.0', '0.0',
                           '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0']
            ###################################################################################################
            # School Courses
            scourses = SchoolCourse.objects.filter(
                ref_school=school_user.ref_school.id).values_list('title')
            scourses = [c[0] for c in scourses]
            # School Services
            ssercices = SchoolService.objects.filter(
                ref_school=school_user.ref_school.id).values_list('service_name')
            ssercices = [c[0] for c in ssercices]
            ssercices = list(set(ssercices))
            # print(ssercices)
            # print(scourses)

            for s_exp in s_expenses:
                year = int(s_exp.get("year"))

                if year_wise_data.get(year) is None:
                    year_wise_data.setdefault(year, {})
                    if int(year) == int(current_day.strftime('%Y')):
                        current_month = int(current_day.strftime('%m'))
                    else:
                        current_month = 12

                    year_wise_data[year].setdefault(
                        "months", months_list[12-current_month:])
                    year_wise_data[year].setdefault(
                        "total_expenses", amount_list[12-current_month:])
                    year_wise_data[year].setdefault(
                        "total_earnings", amount_list[12-current_month:])
                    year_wise_data[year].setdefault(
                        "total_course_expenses", amount_list[12-current_month:])
                    year_wise_data[year].setdefault(
                        "total_course_earnings", amount_list[12-current_month:])

                    year_wise_data[year].setdefault("course_expenses", {})
                    year_wise_data[year].setdefault("course_earnings", {})

                    for course in scourses:
                        year_wise_data[year]["course_expenses"].setdefault(
                            course, amount_list[12-current_month:])
                        year_wise_data[year]["course_earnings"].setdefault(
                            course, amount_list[12-current_month:])

                    year_wise_data[year].setdefault(
                        "total_service_expenses", amount_list[12-current_month:])
                    year_wise_data[year].setdefault(
                        "total_service_earnings", amount_list[12-current_month:])

                    year_wise_data[year].setdefault("service_expenses", {})
                    year_wise_data[year].setdefault("service_earnings", {})

                    for service in ssercices:
                        year_wise_data[year]["service_expenses"].setdefault(
                            service, amount_list[12-current_month:])
                        year_wise_data[year]["service_earnings"].setdefault(
                            service, amount_list[12-current_month:])

                    # year_wise_data[year].setdefault("total_teacher_expenses", amount_list[12-current_month:])
                    # year_wise_data[year].setdefault("total_teacher_earnings", amount_list[12-current_month:])
                    # year_wise_data[year].setdefault("total_other_expenses", amount_list[12-current_month:])
                    # year_wise_data[year].setdefault("total_other_earnings", amount_list[12-current_month:])

            for s_ear in s_earnings:
                year = int(s_ear.get("year"))

                if year_wise_data.get(year) is None:
                    year_wise_data.setdefault(year, {})
                    if int(year) == int(current_day.strftime('%Y')):
                        current_month = int(current_day.strftime('%m'))
                    else:
                        current_month = 12

                    year_wise_data[year].setdefault(
                        "months", months_list[12-current_month:])
                    year_wise_data[year].setdefault(
                        "total_expenses", amount_list[12-current_month:])
                    year_wise_data[year].setdefault(
                        "total_earnings", amount_list[12-current_month:])
                    year_wise_data[year].setdefault(
                        "total_course_expenses", amount_list[12-current_month:])
                    year_wise_data[year].setdefault(
                        "total_course_earnings", amount_list[12-current_month:])

                    year_wise_data[year].setdefault("course_expenses", {})
                    year_wise_data[year].setdefault("course_earnings", {})

                    for course in scourses:
                        year_wise_data[year]["course_expenses"].setdefault(
                            course, amount_list[12-current_month:])
                        year_wise_data[year]["course_earnings"].setdefault(
                            course, amount_list[12-current_month:])

                    year_wise_data[year].setdefault(
                        "total_service_expenses", amount_list[12-current_month:])
                    year_wise_data[year].setdefault(
                        "total_service_earnings", amount_list[12-current_month:])

                    year_wise_data[year].setdefault("service_expenses", {})
                    year_wise_data[year].setdefault("service_earnings", {})

                    for service in ssercices:
                        year_wise_data[year]["service_expenses"].setdefault(
                            service, amount_list[12-current_month:])
                        year_wise_data[year]["service_earnings"].setdefault(
                            service, amount_list[12-current_month:])

                    # year_wise_data[year].setdefault("total_teacher_expenses", amount_list[12-current_month:])
                    # year_wise_data[year].setdefault("total_teacher_earnings", amount_list[12-current_month:])
                    # year_wise_data[year].setdefault("total_other_expenses", amount_list[12-current_month:])
                    # year_wise_data[year].setdefault("total_other_earnings", amount_list[12-current_month:])
            ########################################################################################################

            for s_exp in s_expenses:
                year = int(s_exp.get("year"))

                __month = calendar.month_abbr[s_exp.get("month")]
                if __month in year_wise_data[year]["months"]:
                    _idx = year_wise_data[year]["months"].index(__month)

                    year_wise_data[year]["total_expenses"][_idx] = float(
                        s_exp.get("sum_amount"))

            for s_ear in s_earnings:
                year = int(s_ear.get("year"))

                __month = calendar.month_abbr[s_ear.get("month")]

                if __month in year_wise_data[year]["months"]:
                    _idx = year_wise_data[year]["months"].index(__month)

                    year_wise_data[year]["total_earnings"][_idx] = float(
                        s_ear.get("sum_amount"))

                    if s_ear['sum_discount']:
                        year_wise_data[year]["total_expenses"][_idx] = float(
                            year_wise_data[year]["total_expenses"][_idx]) + float(s_ear['sum_discount'])

            for s_course_exp in s_course_expenses:
                year = int(s_course_exp.get("year"))

                __month = calendar.month_abbr[s_course_exp.get("month")]
                if __month in year_wise_data[year]["months"]:
                    _idx = year_wise_data[year]["months"].index(__month)

                    if s_course_exp['ref_school_course']:
                        year_wise_data[year]["total_course_expenses"][_idx] = float(
                            year_wise_data[year]["total_course_expenses"][_idx]) + float(s_course_exp.get("sum_amount"))

            for s_course_exp in s_course_expenses:
                year = int(s_course_exp.get("year"))

                __month = calendar.month_abbr[s_course_exp.get("month")]
                if __month in year_wise_data[year]["months"]:
                    _idx = year_wise_data[year]["months"].index(__month)

                    course_id = s_course_exp['ref_school_course']
                    if s_course_exp['ref_school_course']:
                        scourse = SchoolCourse.objects.get(pk=course_id)
                        year_wise_data[year]["course_expenses"][scourse.title][_idx] = float(
                            s_course_exp.get("sum_amount"))

            for s_course_ear in s_course_earnings:
                year = int(s_course_ear.get("year"))

                __month = calendar.month_abbr[s_course_ear.get("month")]
                if __month in year_wise_data[year]["months"]:
                    _idx = year_wise_data[year]["months"].index(__month)

                    _course = s_course_ear['ap_course_name']
                    if s_course_ear['ap_course_name']:
                        year_wise_data[year]["course_earnings"][_course][_idx] = float(
                            s_course_ear.get("sum_amount"))

            for s_service_exp in s_service_expenses:
                year = int(s_service_exp.get("year"))

                __month = calendar.month_abbr[s_service_exp.get("month")]
                if __month in year_wise_data[year]["months"]:
                    _idx = year_wise_data[year]["months"].index(__month)

                    service_id = s_service_exp['ref_school_service']
                    if s_service_exp['ref_school_service']:
                        service = SchoolService.objects.get(pk=service_id)
                        # print(year, __month, _idx, service_id, service.service_name)
                        year_wise_data[year]["service_expenses"][service.service_name][_idx] = float(
                            year_wise_data[year]["service_expenses"][service.service_name][_idx]) + float(s_service_exp.get("sum_amount"))

            print('\n\n')
            for s in school_earnings:
                year = int(s.year)

                __month = calendar.month_abbr[int(s.created_at.strftime('%m'))]

                service_json_data = s.ap_service_json_data
                ser = service_json_data.replace("'", '"')
                y = json.loads(ser)

                if __month in year_wise_data[year]["months"]:
                    _idx = year_wise_data[year]["months"].index(__month)

                    for idx, data in enumerate(y):
                        perweek = data['perweek']
                        onetime = data['onetime']
                        if perweek:
                            for week in perweek:
                                print(year_wise_data[year])
                                service_name = week['p_service_name']
                                service_price_total = week['p_service_price_total']
                                try:
                                    year_wise_data[year]["service_earnings"][service_name][_idx] = float(
                                        year_wise_data[year]["service_earnings"][service_name][_idx]) + float(service_price_total)
                                except:
                                    pass

                                # print(year, __month, _idx, service_name, service_price_total)
                        if onetime:
                            for otime in onetime:
                                service_name = otime['service_name']
                                service_price_total = otime['service_price_total']
                                year_wise_data[year]["service_earnings"][service_name][_idx] = float(
                                    year_wise_data[year]["service_earnings"][service_name][_idx]) + float(service_price_total)

                                # print(year, __month, _idx, service_name, service_price_total)

            print('\n\n')

            for s_service_exp in s_service_expenses:
                year = int(s_course_exp.get("year"))

                __month = calendar.month_abbr[s_service_exp.get("month")]
                if __month in year_wise_data[year]["months"]:
                    _idx = year_wise_data[year]["months"].index(__month)

                    if s_service_exp['ref_school_service']:
                        year_wise_data[year]["total_service_expenses"][_idx] = float(
                            year_wise_data[year]["total_service_expenses"][_idx]) + float(s_service_exp.get("sum_amount"))

            # for s_teacher_exp in s_teacher_expenses:
            # 	year = int(s_course_exp.get("year"))

            # 	__month = calendar.month_abbr[s_teacher_exp.get("month")]
            # 	if __month in year_wise_data[year]["months"]:
            # 		_idx = year_wise_data[year]["months"].index(__month)

            # 		if s_teacher_exp['ref_school_teacher']:
            # 			year_wise_data[year]["total_teacher_expenses"][_idx] = float(year_wise_data[year]["total_teacher_expenses"][_idx]) + float(s_teacher_exp.get("sum_amount"))

            # for s_other_exp in s_other_expenses:
                # year = int(s_course_exp.get("year"))

                # __month = calendar.month_abbr[s_other_exp.get("month")]
                # if __month in year_wise_data[year]["months"]:
                # 	_idx = year_wise_data[year]["months"].index(__month)

                # 	if s_other_exp['internal_expense_type'] == 'Other':
                # 		year_wise_data[year]["total_other_expenses"][_idx] = float(year_wise_data[year]["total_other_expenses"][_idx]) + float(s_other_exp.get("sum_amount"))

            context = {
                "year_wise_data": year_wise_data,
            }

            print('\n', year_wise_data)

            return context
            ###### End Track School Expenses #####

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        aplication = self.aplication_get_data()
        year = self.aplication_get_data_by_year()
        expenses = self.expenses_get_data()
        print("=========================")
        print(year)

        # For Application Status
        application_status_graph = [
            ['Status', 'Records'],
            ['Accepted', 0],
            ['Pending', 0],
            ['Rejected', 0],
        ]
        for idx, level in enumerate(aplication.get('level')):
            if level == 'Accepted':
                application_status_graph[1][1] = aplication.get('value')[idx]
            elif level == 'Pending':
                application_status_graph[2][1] = aplication.get('value')[idx]
            elif level == 'Rejected':
                application_status_graph[3][1] = aplication.get('value')[idx]
            # application_status_graph.append([level, aplication.get('value')[idx]])

        # End For Application Status
        
        # For Geo Map
        app_country_queryset = Application.objects.all().values('ap_country').annotate(total=Count('ap_country'))
        
        application_country_wise =[['Country', 'Application'],]
        for qset in app_country_queryset:
            application_country_wise.append(
                [qset.get('ap_country'), qset.get('total')]
            )
        # End For Geo Map

        transactions = Transaction.objects.all().annotate(
                year=ExtractYear(F('created_at')),
                month=ExtractMonth(F('created_at')),
            )
        tansaction_monthly= transactions.values('year', 'month').annotate(total=Count('month'),).order_by('month')
        
        transcations_list = [["Year-Month", "Application"],]
        for t in tansaction_monthly:
            transcations_list.append(
                [f"{t.get('year')}-{t.get('month')}", t.get('total')]
            )

        print(transcations_list)
        context['application'] = aplication
        context['transcations_list'] = json.dumps(transcations_list)
        context['year'] = year
        context['expenses'] = json.dumps(expenses, sort_keys=True)

        context['total_organizations'] = Organization.objects.count()
        context['total_countries'] = Country.objects.count()
        context['total_cities'] = City.objects.count()
        context['total_schools'] = School.objects.count()
        context['total_users'] = User.objects.count()

        context['application_status_graph'] = json.dumps(application_status_graph)
        context['application_country_wise'] = json.dumps(application_country_wise)
        return context


@login_required
def school_student_dashboard(request):
    user = request.user
    current_date = timezone.now().date()
    if user.groups.filter(name='school_student').exists():
        school = request.user.schoolstudentuserprofile.ref_school.id
        school_model = School.objects.get(id=school)
        if school_model:
            context = {}
            student = SchoolStudentUserProfile.objects.get(ref_user=user)
            student_course = StudentProfileHasCourse.objects.filter(
                ref_student=student)
            print(student_course)
            student_accommodation = StudentProfileHasAccommodation.objects.filter(
                ref_student=student)
            student_services = StudentProfileHasService.objects.filter(
                ref_student=student)
            certificate = SchoolCertificate.objects.filter(ref_student=student)
            letters = SchoolLetterSend.objects.filter(ref_student=student)
            
            # installments = student_course.first().installments

            installments = []
            pending_installments = []
            pay_now = True
            for course in student_course:
                for installment in course.installments:
                    installment_date = datetime.strptime(installment['date'], '%Y-%m-%d').date()
                    
                    if installment['status'] == "Done":
                        status = 'Done'
                    elif installment['status'] == "Pending":
                        if pay_now:
                            status = 'Pay Now'
                            pay_now = False
                        else:
                            status = 'Pay Later'

                    if installment['status'] == "Pending" and current_date >= installment_date:
                        pending_installments.append(installment)


                    installments.append((status,installment, course))



            # print (student)
            context['school'] = school_model
            context['student'] = student
            context['student_course'] = student_course
            context['student_accommodation'] = student_accommodation
            context['student_services'] = student_services
            context['certificate'] = certificate
            context['letters'] = letters
            context['installments'] = installments
            context['pending_installments'] = pending_installments

            return render(request, 'admin/school_student_dashboard.html', context)
        else:
            permission = "permission"
            return render(request, 'admin/school_student_dashboard.html', {'permission': permission})
    else:
        permission = "permission"
        return render(request, 'admin/school_student_dashboard.html', {'permission': permission})


@login_required
def school_teacher_dashboard(request):
    user = request.user
    if user.groups.filter(name='teacher').exists():
        school = request.user.teacheruserprofile.ref_school.id
        school_model = School.objects.get(id=school)
        if school_model:
            context = {}
            teacher = TeacherUserProfile.objects.get(ref_user=user)
            certificateteacher = CertificateTeacher.objects.filter(
                ref_teacher_user_profile=teacher.id)
            address = UserAddress.objects.filter(ref_user=teacher.ref_user.id)
            contact = UserContact.objects.filter(ref_user=teacher.ref_user.id)
            # print (student)
            context['school'] = school_model
            context['teacher'] = teacher
            context['certificateteacher'] = certificateteacher
            context['address'] = address
            context['contact'] = contact
            context['course'] = SchoolClass.objects.filter(
                ref_teacher_name=user)
            context['schedule'] = SchoolSchedule.objects.filter(
                ref_schedule_school_course__ref_teacher_name=user)
            context['students'] = SchoolStudentUserProfile.objects.filter(
                rel_ref_student_student_profile_has_course__ref_course__ref_teacher_name=user)
            context['exams'] = SchoolExam.objects.filter(
                ref_course__ref_teacher_name=user)
            context['request'] = request
            context['user'] = user

            return render(request, 'admin/school_teacher_dashboard.html', context)
        else:
            permission = "permission"
            return render(request, 'admin/school_teacher_dashboard.html', {'permission': permission})
    else:
        permission = "permission"
        return render(request, 'admin/school_teacher_dashboard.html', {'permission': permission})


'''
STRIPE PAYMENT INTEGRATION
'''


@login_required
def student_service_payment_success(request):
    template_name = 'admin/payment/student_service_success.html'

    service_id = request.GET.get('service')
    accommodation_id = request.GET.get('accommodation')
    installment_ids = request.GET.getlist('installments')
    installment_type = request.GET.get('installment_type')
    class_id = request.GET.get('class')

    context = {
        'transaction_id': '',
    }

    if service_id:
        student_services = get_object_or_404(
            StudentProfileHasService, pk=service_id)
        context['services'] = student_services

    if accommodation_id:
        student_accommodation = get_object_or_404(
            StudentProfileHasAccommodation, pk=accommodation_id)
        context['accommodation'] = student_accommodation

    if installment_ids and class_id:
        student_has_course = get_object_or_404(
            StudentProfileHasCourse, pk=class_id)
        context['installment'] = student_has_course
        context['installment_numbers'] = installment_ids
        
        installment_amounts = 0
        if installment_type == 'full_payment':
            for idx in installment_ids:
                installment_amounts += student_has_course.installments[int(idx)-1]['amount']
        else:
            installment_amounts = student_has_course.installments[0]['amount']        
        
        context['installment_amount'] = installment_amounts

    return render(request=request, template_name=template_name, context=context)


@login_required
def student_service_payment_cancel(request):
    template_name = 'admin/payment/student_service_cancel.html'

    # print(request.GET)
    service_id = request.GET.get('service')
    accommodation_id = request.GET.get('accommodation')
    installment_ids = request.GET.getlist('installments')
    installment_type = request.GET.get('installment_type')
    class_id = request.GET.get('class')

    context = {
        'transaction_id': '',
    }

    if service_id:
        student_services = get_object_or_404(
            StudentProfileHasService, pk=service_id)
        context['services'] = student_services

    if accommodation_id:
        student_accommodation = get_object_or_404(
            StudentProfileHasAccommodation, pk=accommodation_id)
        context['accommodation'] = student_accommodation

    if installment_ids and class_id:
        student_has_course = get_object_or_404(
            StudentProfileHasCourse, pk=class_id)
        context['installment'] = student_has_course
        context['installment_numbers'] = installment_ids
        
        installment_amounts = 0
        if installment_type == 'full_payment':
            for idx in installment_ids:
                installment_amounts += student_has_course.installments[int(idx)-1]['amount']
        else:
            installment_amounts = student_has_course.installments[0]['amount']        
        
        context['installment_amount'] = installment_amounts

    # Checking application payment success status or not
    # if application.ap_payment_status:
    #     return redirect('web:application_list')

    return render(request=request, template_name=template_name, context=context)


@login_required
@csrf_exempt
def create_student_installment_payment_session(request):
    if request.method == 'POST':
        stripe.api_key = settings.STRIPE_SECRET_KEY
        content = json.loads(request.body.decode('utf-8'))
        installment_type = content.get('installment_type')
        installment_id = int(content.get('installment_id'))
        class_id = content.get('class_id')
    
        student_has_course = get_object_or_404(
            StudentProfileHasCourse, pk=class_id)
        
        if installment_type == 'full_payment':
            pending_amounts = 0
            full_payment = True

            for installment in student_has_course.installments:
                if installment['status'] == 'Pending':
                    pending_amounts += installment['amount']

            installment_ids = list(range(installment_id, len(student_has_course.installments) + 1))
            installment = student_has_course.installments[-1]
            payment_currency = str(installment['currency'])
            payment_amount = int(pending_amounts)
        else:
            full_payment = False

            installment_ids = [installment_id]
            installment = student_has_course.installments[installment_id - 1]
            payment_currency = str(installment['currency'])
            payment_amount = int(installment['amount'])


        stripe_payment_amount = payment_amount * 100
        customer_email = student_has_course.ref_student.email  # service.ap_email

        try:
            installment_parameters = ''
            for ins_idx in installment_ids:
                installment_parameters += f'installments={ins_idx}&'

            checkout_session = stripe.checkout.Session.create(
                success_url=request.build_absolute_uri(
                    reverse('web:student_service_payment_success')) + f'?installment_type={installment_type}&{installment_parameters}class={class_id}',
                cancel_url=request.build_absolute_uri(
                    reverse('web:student_service_payment_cancel')) + f'?installment_type={installment_type}&{installment_parameters}class={class_id}',

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
                    "full_payment": full_payment,
                    "installment_id": installment_id,
                    "class_id": class_id,
                    "user_id": request.user.id
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


@login_required
@csrf_exempt
def create_student_service_payment_session(request):
    if request.method == 'POST':
        stripe.api_key = settings.STRIPE_SECRET_KEY
        content = json.loads(request.body.decode('utf-8'))
        service_id = content.get('service_id')

        service = get_object_or_404(
            StudentProfileHasService, pk=service_id)

        payment_currency = str(
            service.ref_service.ref_school.ref_currency.currency_short)
        payment_amount = int(service.calculate_amount)
        stripe_payment_amount = payment_amount * 100
        customer_email = service.ref_student.email  # service.ap_email

        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=request.build_absolute_uri(
                    reverse('web:student_service_payment_success')) + f'?service={service_id}',
                cancel_url=request.build_absolute_uri(
                    reverse('web:student_service_payment_cancel')) + f'?service={service_id}',

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
                    "service_id": service.id,
                    "user_id": request.user.id
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


@login_required
@csrf_exempt
def create_student_accommodation_payment_session(request):
    if request.method == 'POST':
        stripe.api_key = settings.STRIPE_SECRET_KEY
        content = json.loads(request.body.decode('utf-8'))
        accommodation_id = content.get('accommodation_id')

        accommodation = get_object_or_404(
            StudentProfileHasAccommodation, pk=accommodation_id)

        payment_currency = str(
            accommodation.ref_accommodation_room.ref_school.ref_currency.currency_short)
        payment_amount = int(accommodation.calculate_amount)
        stripe_payment_amount = payment_amount * 100
        customer_email = accommodation.ref_student.email

        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=request.build_absolute_uri(
                    reverse('web:student_service_payment_success')) + f'?accommodation={accommodation_id}',
                cancel_url=request.build_absolute_uri(
                    reverse('web:student_service_payment_cancel')) + f'?accommodation={accommodation_id}',

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
                    "accommodation_id": accommodation.id,
                    "user_id": request.user.id
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
