from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Document)
admin.site.register(Student)
admin.site.register(Record)
admin.site.register(StudentInfo)
admin.site.register(Version)