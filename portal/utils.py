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

    return {"student": info, "records": records, "admission_no": admission_no, "versions": version_values, "cur_ver": version.version_count, "user": version.curr_user, "date": version.date, "lock": student.lock}


def split_records(records):

    ordered_records = {"set1": [], "set2": []}
    labels = ["set1", "set2"]    
    cur_set = 0
    item_index = 1
    bin_size = len(records) // 2 + 1

    for rec in records:

        # Chunking logic
        if item_index % bin_size == 0:
            item_index=1
            cur_set += 1
            if cur_set >= len(labels):
                cur_set = len(labels) - 1
                
        ordered_records[labels[cur_set]].append(rec)
        item_index += 1
    len_1, len_2 = len(ordered_records["set1"]), len(ordered_records["set2"])
    print(ordered_records, len_1, len_2, f"bin size: {bin_size}")

    if len_1 - len_2 > 0:
        extra = ordered_records["set1"][-1]
    elif len_1 - len_2 == 0:
        extra = []
    else:
        extra = ordered_records["set2"][-1]

    ordered_records = zip(ordered_records["set1"], ordered_records["set2"])
    serial_numbers = list(zip([i for i in range(1, len_1 + 1)],[i for i in range(len_1 + 1, len_1 + len_2 + 1)]))
    len_extra = len_1 + len_2

    # Collecting the elements as tuples
    return ordered_records, extra, serial_numbers, len_extra


def mail_student(template, context, to_addr):

    subject = f'kg submitted doc version {context["cur_ver"]}'
    html_message = render_to_string(template, context)
    plain_message = strip_tags(html_message)
    from_email = EMAIL_HOST_USER

    send_mail(subject, plain_message, from_email, [to_addr], html_message=html_message)


