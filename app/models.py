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
    student = models.ForeignKey(StudentModel, related_name="enrolled_student", on_delete=models.CASCADE)
    subject_1 = models.ForeignKey(SubjectModel, related_name="enrolled_subject_1", on_delete=models.CASCADE)
    subject_2 = models.ForeignKey(SubjectModel, related_name="enrolled_subject_2", on_delete=models.CASCADE)
    subject_3 = models.ForeignKey(SubjectModel, related_name="enrolled_subject_3", on_delete=models.CASCADE)
    def __str__(self):
        return self.student.name

