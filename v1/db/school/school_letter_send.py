import imp
from django.db import models

from v1.base.models import BaseModel, BaseModelMeta

from django.contrib.auth.models import User
from .school_letter import SchoolLetter
from ..user.profile import SchoolStudentUserProfile

from v1.base.configs import cRequest

class SchoolLetterSend(BaseModel, models.Model):
	ref_letter = models.ForeignKey( SchoolLetter , related_name="rel_school_letter_school_letter_content" , on_delete=models.CASCADE )
	
	content = models.TextField(blank=True,null=True)
	submit_date = models.DateField(blank=True,null=True)

	ref_submit_by = models.ForeignKey(User, related_name="rel_school_letter_school_user" ,on_delete=models.CASCADE, blank=True, null=True )
	ref_student = models.ForeignKey( SchoolStudentUserProfile , related_name="rel_school_letter_school_student" , on_delete=models.CASCADE )

	Meta = BaseModelMeta( attr={"db_table": "school_letter_send"}, app_name='db' )

	def __str__(self):
		return '%s' % self.ref_letter