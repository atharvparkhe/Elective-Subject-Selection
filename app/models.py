from django.db import models
from base.models import BaseModel
from authentication.models import StudentModel


class SubjectModel(BaseModel):
    name = models.CharField(max_length=50)
    desc = models.TextField()
    syllabus = models.URLField(max_length=200)
    def __str__(self):
        return self.name


class EnollmentModel(BaseModel):
    subject = models.ForeignKey(SubjectModel, related_name="enrolled_subject", on_delete=models.CASCADE)
    student = models.ForeignKey(StudentModel, related_name="enrolled_student", on_delete=models.CASCADE)
    def __str__(self):
        return self.student.name

