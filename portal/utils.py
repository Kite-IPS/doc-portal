from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from doc_portal.settings import EMAIL_HOST_USER
from .models import *



def get_student_info(request, admission_no):

    # Loading the student info
    student = get_object_or_404(Student, admission_no=admission_no)
    if 'version' in request.GET:
        version = int(request.GET.dict()["version"])
    else:
        version = student.version_count
    version = get_object_or_404(Version, version_count=version, student=student)
    info = get_object_or_404(StudentInfo, student=student, ver=version.stud_ver)
    records = Record.objects.filter(student=student, ver=version.docs_ver)
    version_values = [i + 1 for i in range(0, student.version_count+1)]

    return {"student": info, "records": records, "admission_no": admission_no, "versions": version_values, "cur_ver": version.version_count, "user": version.curr_user}


def mail_student(template, context, to_addr):

    subject = f'kg submitted doc version {context["cur_ver"]}'
    html_message = render_to_string(template, context)
    plain_message = strip_tags(html_message)
    from_email = EMAIL_HOST_USER

    send_mail(subject, plain_message, from_email, [to_addr], html_message=html_message)


