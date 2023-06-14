from django.db import models
from base.models import *


class DepartmentModel(BaseModel):
    name = models.CharField(max_length=50)
    time_table = models.ImageField(upload_to="time-table", height_field=None, width_field=None, max_length=None, null=True, blank=True)
    def __str__(self):
        return self.name


class StudentModel(BaseUser):
    roll_no = models.CharField(max_length=50)
    profile_pic = models.ImageField(upload_to="student", height_field=None, width_field=None, max_length=None, null=True, blank=True)
    department = models.ForeignKey(DepartmentModel, related_name="student_department", on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class TeacherModel(BaseUser):
    post = models.CharField(max_length=50)
    experience = models.FloatField(default=1.0)
    profile_pic = models.ImageField(upload_to="teacher", height_field=None, width_field=None, max_length=None, null=True, blank=True)
    department = models.ForeignKey(DepartmentModel, related_name="department_teacher", on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class AdminModel(BaseUser):
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        self.is_staff = True
        super(AdminModel, self).save(*args, **kwargs) 


class FileModel(BaseModel):
    file = models.FileField(upload_to="upload", max_length=100)
    def __str__(self):
        return self.file
