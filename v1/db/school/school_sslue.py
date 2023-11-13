from django.db import models

from v1.base.models.model import BaseModel, BaseModelMeta
from v1.db.master.school import School
from v1.db.master.school_class import SchoolClass
from v1.db.school.school_exam import SchoolExam
from v1.db.user.profile import SchoolStudentUserProfile


class SelectiveStudentExam(BaseModel, models.Model):   
    ref_school = models.ForeignKey( School , related_name="rel_ref_school_selective_student_exam" , on_delete=models.CASCADE )
    ref_course = models.ForeignKey( SchoolClass , related_name="rel_ref_course_selective_student_exam" , on_delete=models.CASCADE )
    ref_exam = models.ForeignKey( SchoolExam , related_name="rel_ref_exam_selective_student_exam" , on_delete=models.CASCADE )
    ref_student = models.ManyToManyField( SchoolStudentUserProfile )
    # exam_date = models.DateField(verbose_name="Exam Date")

    Meta = BaseModelMeta( 
        attr={
            "db_table": "selective_student_exam",
        }, 
        app_name='db'
    )

    def __str__(self) -> str:
        return self.ref_exam.title
    
    @property
    def all_students(self):
        return [student.ref_user.username for student in self.ref_student.all()]