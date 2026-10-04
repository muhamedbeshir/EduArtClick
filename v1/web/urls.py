from django.urls import path
from v1.web.views.admin.calender.views import SchoolCalendarView, TeacherCalendarView
from v1.web.views.admin.commission.views import AddAgentCommission, AgentCommissionList, CommissionList, DeleteAgentCommission, EditAgentCommission
from v1.web.views.admin.dashboard_view import create_student_accommodation_payment_session, create_student_installment_payment_session, create_student_service_payment_session, student_service_payment_cancel, student_service_payment_success
from v1.web.views.admin.master.group.views import AddGroup, DeleteGroup, ListGroup, UpdateGroup
from v1.web.views.admin.master.school.classes.views import DeleteSchoolClass, SchoolClassDetails, create_school_class, update_school_class
from v1.web.views.admin.master.school.discount.views import SchoolCourseDiscountCreateView, SchoolCourseDiscountDeleteView, SchoolCourseDiscountEditView
from v1.web.views.admin.master.school.exam.start.views import SchoolExamList, StartExam
from v1.web.views.admin.master.school.expenses.views import SchoolExpenseCreateView, SchoolExpenseDeleteView, SchoolExpenseEditView
from v1.web.views.admin.master.school.payroll.views import SchoolPayrollCreateView, SchoolPayrollDeleteView, SchoolPayrollEditView
from v1.web.views.admin.master.school.setting.views import SchoolSettingCreateView, SchoolSettingListView, SchoolSettingDeleteView, SchoolSettingEditView
from v1.web.views.admin.master.school.sslue.views import AddSelectiveSchoolExam, DeleteSelectiveSchoolExam
from v1.web.views.admin.master.school.student.views import create_student_service, delete_student_service, get_installment_details, get_school_service, update_student_service
from v1.web.views.admin.master.timetable.views import CreateClassTimeTable, CreateClasssTimeTable, DeleteClassTimeTable, UpdateClassTimeTable, check_available_schedule, get_class_timetable, get_classes
from v1.web.views.admin.master.school.sponsor.views import CreateSchoolSponsor, UpdateSchoolSponsor, DeleteSchoolSponsor
from v1.web.views.admin.master.installment.views import CreateSchoolClassInstallment, UpdateSchoolClassInstallment, DeleteSchoolClassInstallment

from .views.home import (
    HomeView, AboutView, ServicesView, ServiceDetailsView, CoursesView,
    CourseDetailsView, ProjectsView, ProjectDetailsView, BlogView,
    BlogDetailsView, FaqView, PricingView, TeamView, TeamDetailsView,
    EventsView, EventDetailsView, ShopView, ShopDetailsView, ContactView,
    ThankYouView, SchoolsView, SchoolDetailsView,
)

from v1.web.views.auth.signup.views import edit_admin_user, edit_organization_user, edit_school_user, edit_staff_user, edit_student_user, edit_agent_user
from .views.admin.application.views import DownloadApprovedLetter, DownloadPaymentInvoice, DownloadTransactionPDF, create_payment_session, webhook, payment_cancel, payment_success
from .views import *
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'web'
urlpatterns = [

    path('', HomeView.as_view(), name='home'),
    path('home/', HomeView.as_view()),

    path('about/', AboutView.as_view(), name='about'),
    path('services/', ServicesView.as_view(), name='services'),
    path('services/<int:pk>/', ServiceDetailsView.as_view(), name='service_details'),
    path('courses/', CoursesView.as_view(), name='courses'),
    path('courses/<int:pk>/', CourseDetailsView.as_view(), name='course_details'),
    path('projects/', ProjectsView.as_view(), name='projects'),
    path('projects/<int:pk>/', ProjectDetailsView.as_view(), name='project_details'),
    path('schools/', SchoolsView.as_view(), name='schools'),
    path('schools/<int:pk>/', SchoolDetailsView.as_view(), name='school_details'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('blog-details/', BlogDetailsView.as_view(), name='blog_details'),
    path('faq/', FaqView.as_view(), name='faq'),
    path('pricing/', PricingView.as_view(), name='pricing'),
    path('team/', TeamView.as_view(), name='team'),
    path('team-details/', TeamDetailsView.as_view(), name='team_details'),
    path('events/', EventsView.as_view(), name='events'),
    path('event-details/', EventDetailsView.as_view(), name='event_details'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('shop-details/', ShopDetailsView.as_view(), name='shop_details'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('thank-you/', ThankYouView.as_view(), name='thank_you'),

    path('login/', login_page, name='login_page'),
#     path('school-student-login', school_student_login,
#          name='school_student_login'),
    path('registration', RegistrationPage.as_view(), name='registration_page'),
    # path('sign-up', sign_up, name='sign_up'),
    path('sign-up-student', sign_up_student, name='sign_up_student'),
    path('sign-up-aggent', sign_up_aggent, name='sign_up_aggent'),
    path('pwd-reset/<token>', AuthForgetPasswordViewset.as_view(), name='pwd_reset'),
    path('forget-password', password_reset_request, name='forget_password'),
    path('forget-password/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='auth/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', MyPasswordResetView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='auth/password_reset_complete.html'), name='password_reset_complete'),

    path('dashboard/master/school/exam/type/add',
         AddSchoolExamType.as_view(), name='school_exam_type_add'),
    path('dashboard/master/school/exam/type/edit/<pk>',
         EditSchoolExamType.as_view(), name='school_exam_type_edit'),
    path('dashboard/master/school/exam/type/delete/<pk>',
         DeleteSchoolExamType.as_view(), name='school_exam_type_delete'),
    path('dashboard/master/school/exam/type/list',
         ListSchoolExamType.as_view(), name='school_exam_type_list'),

    path('dashboard/school/exam/add/<pk>',
         SchoolExamCreate, name='school_exam_create'),

    path('dashboard/school/exam/details/<pk>',
         SchoolExamDetails.as_view(), name='school_exam_details'),

    path('dashboard/school/exam/category/add/<ref_exam_id>',
         AddSchoolExamCategory.as_view(), name='school_exam_category_add'),
    path('dashboard/school/exam/category/delete/<pk>',
         DeleteSchoolExamCategory.as_view(), name='school_exam_category_delete'),

    path('dashboard/school/exam/question/view/<pk>',
         ViewSchoolExamQuestion.as_view(), name='school_exam_question_view'),
    path('dashboard/school/exam/question/add/<ref_exam_id>',
         AddSchoolExamQuestion.as_view(), name='school_exam_question_add'),
    path('dashboard/school/exam/question/delete/<pk>',
         DeleteSchoolExamQuestion.as_view(), name='school_exam_question_delete'),
    path('dashboard/school/exam/start/<app_id>',
         StartSchoolExam.as_view(), name='school_exam_start'),
    path('dashboard/school/exam/result/<pk>',
         UpdateSchoolExamResult.as_view(), name='school_exam_result'),

    path('dashboard/school/letter/type/delete/<pk>',
         DeleteSchoolLetterType.as_view(), name='school_letter_type_delete'),
    path('dashboard/school/letter/type/edit/<pk>',
         EditSchoolLetterType.as_view(), name='school_letter_type_edit'),
    path('dashboard/school/letter/type/<pk>',
         AddSchoolLetterType.as_view(), name='school_letter_type_add'),
    
    path('dashboard/school/letter/<school_id>',
         AddSchoolLetter.as_view(), name='school_letter_add'),
    path('dashboard/school/letter/delete/<pk>',
         DeleteSchoolLetter.as_view(), name='school_letter_delete'),
    path('dashboard/school/letter/edit/<pk>',
         EditSchoolLetter.as_view(), name='school_letter_edit'),
    path('dashboard/school/letter/view/<pk>',
         ViewSchoolLetter.as_view(), name='school_letter_view'),

    path('dashboard/school/certificate/content/add/<int:pk>',
         AddSchoolCertificateContent.as_view(), name='school_cert_add'),
    path('dashboard/school/certificate/content/edit/<pk>',
         EditSchoolCertificateContent.as_view(), name='school_cert_edit'),
    path('dashboard/school/certificate/content/delete/<pk>',
         DeleteSchoolCertificateContent.as_view(), name='school_cert_delete'),
    path('dashboard/school/certificate/content/view/<pk>',
         ViewSchoolCertificateContent.as_view(), name='school_cert_view'),

    path('dashboard/user-permission-change/<pk>/',
         user_permission_change, name='user_permission_change'),
    path('logout', logout_view, name='logout_view'),
    path('dashboard', Dashboard.as_view(), name='dashboard'),
    # path('dashboard', dashboard, name='dashboard'),
    # path('dashboard/add-course', course_create, name='add_course'),
    # path('dashboard/courses', ListCourse.as_view(), name='list_course'),
    # path('dashboard/course/<pk>', DetailCourse.as_view(), name='detail_course'),
    # path('dashboard/edit-course/<pk>', CourseUpdateView.as_view(), name='edit_course'),
    # path('dashboard/delete-course/<pk>', DeleteCourseView.as_view(), name='delete_course'),

    # path('dashboard/add-client', client_create, name='client_create'),
    # path('dashboard/clients', ClientListView.as_view(), name='client_list'),
    # path('dashboard/client/<pk>', ClientDetailView.as_view(), name='client_detail'),
    # path('dashboard/add-client-course/<pk>', ClientCourseView.as_view(), name='add_client_course'),

    # user create in dashboard
    path('dashboard/create-user-page',
         UserCraetePage.as_view(), name='create_user_page'),
    path('dashboard/create-student-user',
         create_student_user, name='create_student_user'),
    path('dashboard/edit-student-user/<pk>',
         edit_student_user, name='edit_student_user'),
    path('dashboard/create-agent-user',
         create_agent_user, name='create_agent_user'),
    path('dashboard/edit-agent-user/<pk>',
         edit_agent_user, name='edit_agent_user'),
    path('dashboard/create-staff-user',
         create_staff_user, name='create_staff_user'),
    path('dashboard/edit-staff-user/<pk>',
         edit_staff_user, name='edit_staff_user'),
    path('dashboard/create-admin-user',
         create_admin_user, name='create_admin_user'),
    path('dashboard/edit-admin-user/<pk>',
         edit_admin_user, name='edit_admin_user'),
    # path('dashboard/delete-student-user/<pk>', DeleteStudent.as_view(), name='delete_student_user'),
    # path('dashboard/delete-agent-user/<pk>', DeleteAgent.as_view(), name='delete_agent_user'),
    # path('dashboard/delete-staff-user/<pk>', DeleteStaffAndAdmin.as_view(), name='delete_staff_user'),
    # path('dashboard/delete-admin-user/<pk>', DeleteStaffAndAdmin.as_view(), name='delete_admin_user'),
    path('dashboard/delete-user/<pk>', DeleteUser.as_view(), name='delete_user'),


    path('dashboard/groups-list',
         ListGroup.as_view(), name='list_group'),
    path('dashboard/add-group',
         AddGroup.as_view(), name='add_group'),
    path('dashboard/update-group/<int:pk>',
         UpdateGroup.as_view(), name='update_group'),
    path('dashboard/delete-group/<int:pk>',
         DeleteGroup.as_view(), name='delete_group'),

    path('dashboard/add-organization',
         AddOrganization.as_view(), name='add_organization'),
    path('dashboard/edit-organization/<pk>',
         EditOrganization.as_view(), name='edit_organization'),
    path('dashboard/organizations-list',
         ListOrganization.as_view(), name='list_organization'),
    path('dashboard/organizations-delete/<pk>',
         DeleteOrganization.as_view(), name='delete_organization'),
    path('dashboard/create-organization-user',
         create_organization_user, name='create_organization_user'),
    path('dashboard/edit-organization-user/<pk>',
         edit_organization_user, name='edit_organization_user'),
    path('dashboard/create-school-user/',
         create_school_user, name='create_school_user'),
    path('dashboard/edit-school-user/<pk>',
         edit_school_user, name='edit_school_user'),

    path('dashboard/add-school-user/<pk>', create_school_user_by_organization,
         name='create_school_user_by_organization'),
    path('dashboard/list-school-user/<pk>', organization_school_user_list,
         name='organization_school_user_list'),

    path('dashboard/organization-create-school/<pk>',
         organization_school_create_view, name='organization_school_create_view'),
    path('dashboard/organization-application-list/<pk>',
         organization_application_list, name='organization_application_list'),
    path('dashboard/school-application-list/<pk>',
         school_application_list, name='school_application_list'),


    path('dashboard/country-list', ListCountry.as_view(), name='country_list'),

    path('dashboard/add-country', AddCountry.as_view(), name='add_country'),
    path('dashboard/country-edit/<pk>',
         EditCountry.as_view(), name='edit_country'),
    path('dashboard/country-list', ListCountry.as_view(), name='country_list'),
    path('dashboard/country-delete/<pk>',
         DeleteCountry.as_view(), name='delete_country'),

    path('dashboard/add-city', AddCity.as_view(), name='add_city'),
    path('dashboard/city-edit/<pk>', EditCity.as_view(), name='edit_city'),
    path('dashboard/city-list', ListCity.as_view(), name='city_list'),
    path('dashboard/city-delete/<pk>', DeleteCity.as_view(), name='delete_city'),

    path('dashboard/create-school', SchoolCreateView.as_view(), name='add_school'),
    path('dashboard/edit-school/<pk>', EditSchool.as_view(), name='edit_school'),
    path('dashboard/school-list', ListSchool.as_view(), name='school_list'),
    path('dashboard/delete-school/<pk>',
         DeleteSchool.as_view(), name='delete_school'),
    path('dashboard/school-detail/<pk>',
         DetailSchool.as_view(), name='deatil_school'),


    path('dashboard/add-school-service/<pk>',
         create_school_service, name='create_school_service'),
    path('dashboard/edit-school-service/<pk>',
         EditSchoolService.as_view(), name='edit_school_service'),
    path('dashboard/delete-school-service/<pk>',
         DeleteSchoolService.as_view(), name='delete_school_service'),

    # accommodation part
    path('dashboard/add-school-accommodation-type/<pk>',
         create_school_accommodation_type, name='create_school_accommodation_type'),
    path('dashboard/edit-school-accommodation-type/<pk>',
         edit_school_accommodation_type, name='edit_school_accommodation_type'),
    path('dashboard/delete-school-accommodation-type/<pk>',
         delete_school_accommodation_type, name='delete_school_accommodation_type'),

    path('dashboard/add-school-accommodation-owner/<pk>',
         create_school_accommodation_owner, name='create_school_accommodation_owner'),
    path('dashboard/add-school-accommodation-owner-next-page-room/<pk>',
         create_school_accommodation_owner_next_page_room, name='create_school_accommodation_owner_next_page_room'),
    path('dashboard/detail-school-accommodation-owner/<pk>',
         DetailSchoolAccommodationOwner.as_view(), name='detail_school_accommodation_owner'),
    path('dashboard/delete-school-accommodation-owner/<pk>',
         delete_school_accommodation_owner, name='delete_school_accommodation_owner'),

    path('dashboard/add-school-accommodation-service/<pk>',
         create_school_accommodation_service, name='create_school_accommodation_service'),
    path('dashboard/edit-school-accommodation-service/<pk>',
         edit_school_accommodation_service, name='edit_school_accommodation_service'),
    path('dashboard/delete-school-accommodation-service/<pk>',
         delete_school_accommodation_service, name='delete_school_accommodation_service'),

    path('dashboard/add-school-accommodation-preferance/<pk>',
         create_school_accommodation_preferance, name='create_school_accommodation_preferance'),
    path('dashboard/edit-school-accommodation-preferance/<pk>',
         edit_school_accommodation_preferance, name='edit_school_accommodation_preferance'),
    path('dashboard/delete-school-accommodation-preferance/<pk>',
         delete_school_accommodation_preferance, name='delete_school_accommodation_preferance'),

    path('dashboard/add-school-accommodation-acc-bank/<pk>',
         create_school_accommodation_acc_bank, name='create_school_accommodation_acc_bank'),
    path('dashboard/edit-school-accommodation-acc-bank/<pk>',
         edit_school_accommodation_acc_bank, name='edit_school_accommodation_acc_bank'),
    path('dashboard/delete-school-accommodation-acc-bank/<pk>',
         delete_school_accommodation_acc_bank, name='delete_school_accommodation_acc_bank'),


    path('dashboard/add-school-schedule/<pk>',
         create_school_schedule, name='create_school_schedule'),
    path('dashboard/edit-school-schedule/<pk>',
         edit_school_schedule, name='edit_school_schedule'),
    path('dashboard/delete-school-schedule/<pk>',
         delete_school_schedule, name='delete_school_schedule'),

    path('dashboard/add-school-room/<pk>',
         create_school_room, name='create_school_room'),
    path('dashboard/edit-school-room/<pk>',
         edit_school_room, name='edit_school_room'),
    path('dashboard/delete-school-room/<pk>',
         delete_school_room, name='delete_school_room'),

    path('dashboard/add-school-course-level/<pk>',
         create_school_course_level, name='create_school_course_level'),
    path('dashboard/edit-school-course-level/<pk>',
         edit_school_course_level, name='edit_school_course_level'),
    path('dashboard/delete-school-course-level/<pk>',
         delete_school_course_level, name='delete_school_course_level'),

    path('dashboard/add-school-course-type/<pk>',
         create_school_course_type, name='create_school_course_type'),
    path('dashboard/edit-school-course-type/<pk>',
         edit_school_course_type, name='edit_school_course_type'),
    path('dashboard/delete-school-course-type/<pk>',
         delete_school_course_type, name='delete_school_course_type'),

    path('dashboard/add-school-teacher/<pk>',
         create_teacher_user_by_school, name='create_teacher_user_by_school'),
    path('dashboard/school-teacher/<pk>',
         DetailTeacher.as_view(), name='school_teacher_detail'),
    path('dashboard/edit-school-teacher/<pk>',
         update_teacher, name='update_teacher'),
    path('teacher-dashboard', school_teacher_dashboard,
         name='school_teacher_dashboard'),

    path('dashboard/add-school-student/<pk>', create_school_student_user_by_school,
         name='create_school_student_user_by_school'),
    path('dashboard/add-school-student-by-application-no', create_school_student_user_by_school_by_app_no,
         name='create_school_student_user_by_school_by_app_no'),
    path('dashboard/edit-school-student/<pk>',
         update_school_student, name='update_school_student'),
    path('dashboard/delete-school-student/<pk>',
         delete_school_student, name='delete_school_student'),
    path('dashboard/detail-school-student/<pk>',
         SchoolStudentDetails.as_view(), name='detail_school_student_user'),
    
    path('dashboard/create-student-course/<pk>',
         create_student_course, name='create_student_course'),
    path('dashboard/edit-student-course/<pk>',
         update_student_course, name='update_student_course'),
    path('dashboard/delete-student-course/<pk>',
         delete_student_course, name='delete_student_course'),
    
    path('dashboard/create-student-accommodation/<pk>',
         create_student_accommodation, name='create_student_accommodation'),
    path('dashboard/edit-student-accommodation/<pk>',
         update_student_accommodation, name='update_student_accommodation'),
    path('dashboard/delete-student-accommodation/<pk>',
         delete_student_accommodation, name='delete_student_accommodation'),
    
    path('student-dashboard', school_student_dashboard,
         name='school_student_dashboard'),
    path('student-dashboard/download-certificate/<pk>',
         DownloadCertificatePDF.as_view(), name='certificate_download'),
    path('student-dashboard/calendar', CalendarView.as_view(), name='calender'),

    path('school-dashboard/calendar',
         SchoolCalendarView.as_view(), name='school_calender'),

    path('teacher-dashboard/calendar',
         TeacherCalendarView.as_view(), name='teacher_calender'),


    path('dashboard/add-teacher-certificate/<pk>', create_certificate_teacher_by_school,
         name='create_certificate_teacher_by_school'),
    path('dashboard/edit-teacher-certificate/<pk>',
         edit_certificate_teacher_by_school, name='edit_certificate_teacher_by_school'),
    path('dashboard/delete-teacher-certificate/<pk>',
         delete_certificate_teacher_by_school, name='delete_certificate_teacher_by_school'),

    path('dashboard/add-teacher-address/<pk>', create_teacher_user_address_by_school,
         name='create_teacher_user_address_by_school'),
    path('dashboard/delete-teacher-address/<pk>', delete_teacher_user_address_by_school,
         name='delete_teacher_user_address_by_school'),
    path('dashboard/edit-teacher-address/<pk>', edit_teacher_user_address_by_school,
         name='edit_teacher_user_address_by_school'),
         
    path('dashboard/add-teacher-contact/<pk>', create_teacher_user_contact_by_school,
         name='create_teacher_user_contact_by_school'),
    path('dashboard/delete-teacher-contact/<pk>', delete_teacher_user_contact_by_school,
         name='delete_teacher_user_contact_by_school'),
    path('dashboard/edit-teacher-contact/<pk>', edit_teacher_user_contact_by_school,
         name='edit_teacher_user_contact_by_school'),

    path('dashboard/add-school-course/<pk>',
         create_school_course, name='create_school_course'),
    path('dashboard/edit-school-course/<pk>',
         update_school_course, name='edit_school_course'),
    path('dashboard/delete-school-course/<pk>',
         DeleteSchoolCourse.as_view(), name='delete_school_course'),
    path('dashboard/detail-school-course/<int:pk>',
         SchoolCourseDetails.as_view(), name='details_school_course'),
    # path('dashboard/detail-school-course/<pk>', SchoolCourseDetails.as_view(), name='detail_school_course'),


    path('dashboard/add-school-class/<pk>',
         create_school_class, name='create_school_class'),
    path('dashboard/edit-school-class/<pk>',
         update_school_class, name='edit_school_class'),
    path('dashboard/delete-school-class/<pk>',
         DeleteSchoolClass.as_view(), name='delete_school_class'),
    path('dashboard/detail-school-class/<pk>',
         SchoolClassDetails.as_view(), name='detail_school_course'),

    path('dashboard/add-school-course-price/<pk>',
         create_school_course_price, name='create_school_course_price'),
    path('dashboard/edit-school-course-price/<pk>',
         EditSchoolCoursePrice.as_view(), name='edit_school_course_price'),
    path('dashboard/delete-school-course-price/<pk>',
         DeleteSchoolCoursePrice.as_view(), name='delete_school_course_price'),

    path('dashboard/add-dynamic-school-application-form-field/<pk>',
         create_dynamic_school_application_form_field, name='create_dynamic_school_application_form_field'),


    path('dashboard/add-currency/', create_currency, name='create_currency'),
    path('dashboard/currency-list/', CurrencyList.as_view(), name='currency_list'),


    path('dashboard/admision-form/', course_calculate_cost,
         name='course_calculate_cost'),
    path('dashboard/submit_application_ajax/',
         submit_application, name='submit_application'),

    path('dashboard/application/',
         ApplicationListView.as_view(), name='application_list'),
    path('dashboard/application-delete/<pk>',
         DeleteApplication.as_view(), name='application_delete'),

    path('dashboard/application-approvel/<pk>',
         ApplicationAprovelLetter.as_view(), name='application_aprovel_letter'),
    path('dashboard/application-reject/<pk>',
         ApplicationRejectLetter.as_view(), name='application_reject_letter'),
    path('dashboard/application/<pk>',
         ApplicationDetailView.as_view(), name='application_detail'),
    path('link/application/<token>', ApplicationSendLinkView.as_view(),
         name='application_send_link'),
    path('aplication/succes-message', ApplicationSendLinkSuccesMessage.as_view(),
         name='application_send_link_succes_message'),
    path('download/application/<token>',
         GeneratePDF.as_view(), name='application_download'),
    path('download/application-pdf/<pk>',
         DownloadApplicationPDF.as_view(), name='application_download_pdf'),
    path('download/approved-letter/<pk>',
         DownloadApprovedLetter.as_view(), name='application_approved_letter'),


    path('dashboard/get_application_course_end_date/', get_application_course_end_date, name='get_application_course_end_date'),
    path('dashboard/get_city/', get_city, name='get_city'),
    path('dashboard/get_school_for_org/',
         get_school_for_org, name='get_school_for_org'),

    path('dashboard/get_schools/', get_schools, name='get_schools'),
    path('dashboard/get_school_address/',
         get_school_address, name='get_school_address'),
    path('dashboard/get_course_ajax/', get_course_ajax, name='get_course_ajax'),
    path('dashboard/get_course_type_ajax/',
         get_course_type_ajax, name='get_course_type_ajax'),
    path('dashboard/get_course_class_ajax/',
         get_course_class_ajax, name='get_course_class_ajax'),
    path('dashboard/get_course_class_days_ajax/',
         get_course_class_days_ajax, name='get_course_class_days_ajax'),
    path('dashboard/get_course_class_price_ajax/',
         get_course_class_price_ajax, name='get_course_class_price_ajax'),
    path('dashboard/get_study_period_ajax/',
         get_study_period_ajax, name='get_study_period_ajax'),
    path('dashboard/get_course_discount/',
         get_course_discount, name='get_course_discount'),
    path('dashboard/get_level_ajax/', get_level_ajax, name='get_level_ajax'),
    path('dashboard/get_service_ajax/',
         get_service_ajax, name='get_service_ajax'),
    path('dashboard/get_accommodation_ajax/',
         get_accommodation_ajax, name='get_accommodation_ajax'),
    path('dashboard/get_accommodation_type_ajax/',
         get_accommodation_type_ajax, name='get_accommodation_type_ajax'),
    path('dashboard/get_course_price_ajax/',
         get_course_price_ajax, name='get_course_price_ajax'),

    path('dashboard/api', course_detail_ajax, name='course_detail_ajax'),

    path('dashboard/get_available_teachers_and_rooms/',
         get_available_teachers_and_rooms, name='get_available_teachers_and_rooms'),

    path('dashboard/get_exams_ajax', get_exams_ajax, name='get_exams_ajax'),
    path('dashboard/get_students_ajax',
         get_students_ajax, name='get_students_ajax'),
    path('dashboard/get_course_end_date_ajax',
         get_course_end_date_ajax, name='get_course_end_date_ajax'),

    # Stripe Payment Integration
    path('dashboard/aplication/payment/',
         create_payment_session, name='application_payment'),
    path('dashboard/aplication/payment/success/',
         view=payment_success, name='application_payment_success'),
    path('dashboard/aplication/payment/cancelled/',
         view=payment_cancel, name='application_payment_cancel'),
    # End of Stripe Payment Integration

    path('dashboard/transaction-list/',
         TransactionList.as_view(), name='transaction_list'),
    path('download/transaction-pdf/<pk>',
         DownloadTransactionPDF.as_view(), name='transaction_download_pdf'),

    path('dashboard/school-course-discount-add/<pk>',
         SchoolCourseDiscountCreateView.as_view(), name='add_school_course_discount'),
    path('dashboard/school-course-discount-edit/<pk>',
         SchoolCourseDiscountEditView.as_view(), name='edit_school_course_discount'),
    path('dashboard/school-course-discount-delete/<pk>',
         SchoolCourseDiscountDeleteView.as_view(), name='delete_school_course_discount'),

    path('dashboard/school-expense-add/<pk>',
         SchoolExpenseCreateView.as_view(), name='add_school_expense'),
    path('dashboard/school-expense-edit/<pk>',
         SchoolExpenseEditView.as_view(), name='edit_school_expense'),
    path('dashboard/school-expense-delete/<pk>',
         SchoolExpenseDeleteView.as_view(), name='delete_school_expense'),

    path('dashboard/school-payroll-add/<pk>',
         SchoolPayrollCreateView.as_view(), name='add_school_payroll'),
    path('dashboard/school-payroll-edit/<pk>',
         SchoolPayrollEditView.as_view(), name='edit_school_payroll'),
    path('dashboard/school-payroll-delete/<pk>',
         SchoolPayrollDeleteView.as_view(), name='delete_school_payroll'),

    path('dashboard/school-setting-add/<pk>',
         SchoolSettingCreateView.as_view(), name='add_school_setting'),
    path('dashboard/school-setting-edit/<pk>',
         SchoolSettingEditView.as_view(), name='edit_school_setting'),
    path('dashboard/school-setting-list/<pk>',
         SchoolSettingListView.as_view(), name='list_school_setting'),
    path('dashboard/school-setting-delete/<pk>',
         SchoolSettingDeleteView.as_view(), name='delete_school_setting'),

    path('dashboard/commission-list/',
         CommissionList.as_view(), name='commission_list'),
    path('dashboard/agent-commission-add/',
         AddAgentCommission.as_view(), name='add_agent_commission'),
    path('dashboard/agent-commission-edit/<pk>',
         EditAgentCommission.as_view(), name='edit_agent_commission'),
    path('dashboard/agent-commission-delete/<pk>',
         DeleteAgentCommission.as_view(), name='delete_agent_commission'),

    path('dashboard/agent-commission-list/',
         AgentCommissionList.as_view(), name='agent_commission_list'),

    path('dashboard/school/exam/list/',
         SchoolExamList.as_view(), name='school_exam_list'),
    path('dashboard/student/exam/start/<int:pk>',
         StartExam.as_view(), name='student_exam_start'),

    # Selective Student Level Up Exam
    path('dashboard/school/selective/exam/add/<int:pk>',
         AddSelectiveSchoolExam.as_view(), name='selective_student_exam_add'),
    path('dashboard/school/selective/exam/delete/<int:pk>',
         DeleteSelectiveSchoolExam.as_view(), name='selective_student_exam_delete'),

    path('dashboard/school-time-table-add/<pk>',
         CreateClassTimeTable.as_view(), name='create_school_time_table'),
    path('dashboard/school-time-table-update/<pk>',
         UpdateClassTimeTable.as_view(), name='update_school_time_table'),
    path('dashboard/school-time-table-delete/<pk>',
         DeleteClassTimeTable.as_view(), name='delete_school_time_table'),

    path('dashboard/create-student-service/<pk>',
         create_student_service, name='create_student_service'),
    path('dashboard/edit-student-service/<int:pk>',
         update_student_service, name='update_student_service'),
    path('dashboard/delete-student-service/<int:pk>',
         delete_student_service, name='delete_student_service'),

    path('dashboard/get_classes',
         get_classes, name='get_classes'),
    path('dashboard/get_class_timetable',
         get_class_timetable, name='get_class_timetable'),
    path('dashboard/get_school_service',
         get_school_service, name='get_school_service'),
    path('dashboard/get_installment_details/',
         get_installment_details, name='get_installment_details'),

    path('dashboard/student/installment/payment/',
         create_student_installment_payment_session, name='create_student_installment_payment_session'),
    path('dashboard/student/service/payment/',
         create_student_service_payment_session, name='create_student_service_payment_session'),
    path('dashboard/student/accommodation/payment/',
         create_student_accommodation_payment_session, name='create_student_accommodation_payment_session'),
    path('dashboard/student/payment/success/',
         view=student_service_payment_success, name='student_service_payment_success'),
    path('dashboard/student/payment/cancelled/',
         view=student_service_payment_cancel, name='student_service_payment_cancel'),
     path('download/invoice-pdf/<int:course>/<int:ins>/',
         DownloadPaymentInvoice.as_view(), name='invoice_download_pdf'),

    path('dashboard/school-sponsor-add/<pk>',
         CreateSchoolSponsor.as_view(), name='create_school_sponsor'),
    path('dashboard/school-sponsor-update/<pk>',
         UpdateSchoolSponsor.as_view(), name='update_school_sponsor'),
    path('dashboard/school-sponsor-delete/<pk>',
         DeleteSchoolSponsor.as_view(), name='delete_school_sponsor'),

    path('dashboard/add-school-class-installment/<pk>',
         CreateSchoolClassInstallment.as_view(), name='create_school_class_installment'),
    path('dashboard/update-school-class-installment/<pk>',
         UpdateSchoolClassInstallment.as_view(), name='update_school_class_installment'),
    path('dashboard/delete-school-class-installment/<pk>',
         DeleteSchoolClassInstallment.as_view(), name='delete_school_class_installment'),

     path('dashboard/class-time-table-update/<pk>',
         CreateClasssTimeTable.as_view(), name='create_class_time_table'),
     path('dashboard/available-schedule/',
         check_available_schedule, name='check_available_schedule'),

    # Stripe Webhooks
    path('webhooks/stripe/', webhook, name='webhook'),
    # End of Stripe Webhooks
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
