from django.contrib import admin

from .organization import Organization

from .user import UserProfile,OrganizationUserProfile, StudentUserProfile, TeacherUserProfile, AggentUserProfile, AuthForgetPasswordToken, StudentProfileHasCourse, ContactUs

from .master import *

from .other import Currency

from .application import Application, ApplicationService, ApplicationToken

from .school import SchoolCertificateContent, SchoolCertificate, SchoolLetterSend

from .transaction import Transaction

admin.site.register(Organization)

admin.site.register(UserProfile)
admin.site.register(StudentUserProfile)
admin.site.register(AggentUserProfile)
admin.site.register(OrganizationUserProfile)
admin.site.register(AuthForgetPasswordToken)


admin.site.register(City)
admin.site.register(School)
admin.site.register(SchoolService)
admin.site.register(SchoolAccommodationType)
admin.site.register(SchoolAccommodationOwner)
admin.site.register(SchoolAccommodationService)
admin.site.register(AccommodationRequestNoOfRoom)

admin.site.register(SchoolRoom)
admin.site.register(SchoolCourse)
admin.site.register(DynamicSchoolApplicationFormField)
admin.site.register(SchoolSchedule)
admin.site.register(SchoolCourseLevel)

admin.site.register(Currency)

admin.site.register(Application)
admin.site.register(ApplicationService)
admin.site.register(ApplicationToken)

admin.site.register(StudentProfileHasCourse)

admin.site.register(SchoolCertificateContent)
admin.site.register(SchoolCertificate)

admin.site.register(SchoolLetterSend)
admin.site.register(Transaction)


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    readonly_fields = ('name', 'email', 'subject', 'message', 'status', 'created_at', 'updated_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_filter = ('status',)

    def has_add_permission(self, request):
        return False

