from .views import login_page, school_student_login

from .signup import RegistrationPage, UserCraetePage, create_student_user, create_agent_user, create_staff_user, create_admin_user, sign_up_student, sign_up_aggent, sign_up, AuthForgetPasswordViewset, DeleteStudent, DeleteAgent, DeleteStaffAndAdmin, DeleteUser, \
				create_organization_user, create_school_user, create_school_user_by_organization, create_teacher_user_by_school, create_school_student_user_by_school, create_school_student_user_by_school_by_app_no, user_permission_change

from .logout import logout_view

from .forgetpassword import password_reset_request, MyPasswordResetView

from .address import create_teacher_user_address_by_school, delete_teacher_user_address_by_school, \
		edit_teacher_user_address_by_school
from .contact import create_teacher_user_contact_by_school, delete_teacher_user_contact_by_school, \
		edit_teacher_user_contact_by_school

from .teachercertificate import create_certificate_teacher_by_school, edit_certificate_teacher_by_school, delete_certificate_teacher_by_school