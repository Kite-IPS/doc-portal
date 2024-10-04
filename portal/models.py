from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone 

class Document(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.name}"


class Student(models.Model):

    admission_no = models.CharField(max_length=30, unique=True)
    version_count = models.IntegerField()
    lock = models.BooleanField()

    def __str__(self):
        return f"{self.admission_no} - {self.version_count}"


class StudentInfo(models.Model):

    name = models.CharField(max_length=50)
    email = models.EmailField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    department = models.CharField(max_length=50)  
    student_number = models.CharField(max_length=20)   
    parent_name = models.CharField(max_length=50)  
    parent_number = models.CharField(max_length=20)
    quota = models.BooleanField()
    ver = models.IntegerField()

    def __str__(self):
        return f"{self.student.admission_no} - {self.name}"
    

class Record(models.Model):

    ver = models.IntegerField()
    date = models.DateField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    original = models.BooleanField()
    photocopy = models.BooleanField()
    count = models.IntegerField()
    document= models.ForeignKey(Document, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.admission_no} - {self.document.name} - {self.ver}"
    
class Version(models.Model):

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    version_count = models.IntegerField()
    docs_ver = models.IntegerField()
    stud_ver = models.IntegerField()
    curr_user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.admission_no} - {self.version_count} - {self.curr_user}"