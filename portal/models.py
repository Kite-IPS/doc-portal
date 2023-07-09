from django.db import models


class Document(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.name}"


class Student(models.Model):

    admission_no = models.CharField(max_length=30)
    stud_ver = models.IntegerField()
    docs_ver = models.IntegerField()

    def __str__(self):
        return f"{self.admission_no} - {self.stud_ver} - {self.docs_ver}"


class StudentInfo(models.Model):

    name = models.CharField(max_length=50)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    department = models.CharField(max_length=50)  
    student_number = models.CharField(max_length=20)   
    parent_name = models.CharField(max_length=50)  
    parent_number = models.CharField(max_length=20)
    quota = models.BooleanField()
    ver = models.IntegerField()

    def __str__(self):
        return f"{self.recipt_no} - {self.name}"
    

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