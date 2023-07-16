from django.db import models
from base.models import BaseModel
from authentication.models import *


class ContactUs(models.Model):
    name = models.CharField(max_length = 100)
    email = models.EmailField(max_length = 100)
    msg = models.TextField()
    def __str__(self):
        return self.name


class StatusModel(models.Model):
    status = models.CharField(max_length=10)
    img = models.ImageField(upload_to="status", height_field=None, width_field=None, max_length=None)
    def __str__(self):
        return self.status


class SubjectModel(BaseModel):
    name = models.CharField(max_length=50)
    desc = models.TextField()
    cover_img = models.ImageField(upload_to="subject", height_field=None, width_field=None, max_length=None)
    department = models.ForeignKey(DepartmentModel, related_name="department_subject", on_delete=models.CASCADE)
    teacher = models.OneToOneField(TeacherModel, related_name="subject_teacher", on_delete=models.PROTECT, null=True, blank=True)
    syllabus = models.URLField(max_length=200)
    intro = models.URLField(max_length=200)
    def __str__(self):
        return self.name


class EnollmentModel(BaseModel):
    student = models.OneToOneField(StudentModel, related_name="enrolled_students", on_delete=models.CASCADE)
    subject_1 = models.ForeignKey(SubjectModel, related_name="enrolled_subject_1", on_delete=models.CASCADE)
    subject_2 = models.ForeignKey(SubjectModel, related_name="enrolled_subject_2", on_delete=models.CASCADE, null=True, blank=True)
    subject_3 = models.ForeignKey(SubjectModel, related_name="enrolled_subject_3", on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.student.name


class ChangeElectiveModel(BaseModel):
    student = models.ForeignKey(StudentModel, related_name="student_change_elective", on_delete=models.CASCADE)
    from_sub = models.ForeignKey(SubjectModel, related_name="from_subject", on_delete=models.CASCADE)
    to_sub = models.ForeignKey(SubjectModel, related_name="to_subject", on_delete=models.CASCADE)
    teacher_1_decision = models.ForeignKey(StatusModel, related_name="teacher_1_decision", on_delete=models.CASCADE)
    teacher_2_decision = models.ForeignKey(StatusModel, related_name="teacher_2_decision", on_delete=models.CASCADE)
    final_decision = models.ForeignKey(StatusModel, related_name="teacher_3_decision", on_delete=models.CASCADE)
    def __str__(self):
        return self.student.name


