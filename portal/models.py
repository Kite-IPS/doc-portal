from typing import Any
from django.db import models


# Create your models here.
class Document(models.Model):

    name = models.CharField(max_length=10)

    def __str__(self) -> str:
        return f"{self.name}"


class Student(models.Model):

    name = models.CharField(max_length=50)
    roll_no = models.CharField(unique=True, max_length=20)

    def __str__(self):
        return f"{self.roll_no} - {self.name}"
    

class Record(models.Model):

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    original = models.BooleanField()
    photocopy = models.BooleanField()
    count = models.IntegerField()