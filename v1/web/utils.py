# Checking User's Permission, one school can't access other school data

from django.core.exceptions import PermissionDenied



def CHECK_USER_PERMISSION(request, school:object):
    user = request.user
    raise_permission_denied = False

    # a school can't access other school data
    if user.groups.filter(name='school').exists():
        current_school_id = user.organizationuserprofile.ref_school.id

        if not (current_school_id == school.id):
            raise_permission_denied = True
    
    # an organization can't access other organization data
    elif user.groups.filter(name='organization').exists():
        current_organization_id = user.organizationuserprofile.ref_organization.id
        print(current_organization_id, school.ref_organization.id)
        if not (current_organization_id == school.ref_organization.id):
            raise_permission_denied = True
    
    # a school student can't access other school student data
    elif user.groups.filter(name='school_student').exists():
        current_school_id = user.schoolstudentuserprofile.ref_school.id

        if not (current_school_id == school.id):
            raise_permission_denied = True
    
    elif user.groups.filter(name='teacher').exists():
        current_school_id = user.teacheruserprofile.ref_school.id

        if not (current_school_id == school.id):
            raise_permission_denied = True
    

    if raise_permission_denied:
        raise PermissionDenied()
