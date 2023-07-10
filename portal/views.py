from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from .models import *
from datetime import datetime


def home(request):
    if request.method == "POST":
        
        # Getting the data from post request
        post_data = request.POST.dict()
        print(post_data)
        quota = post_data['quota'] == 'govt'
        
        # Creating an entry for the student admission num on first submit
        student = Student(admission_no=post_data['receipt'],
                          version_count=0)
        student.save()

        version = Version(student=student,
                          stud_ver=0,
                          docs_ver=0)
        version.save()

        # Saving the student info
        student_info = StudentInfo(
                              name=post_data['name_stu'],
                              student = student,
                              parent_name=post_data['name_prnt'],
                              department=post_data['dept'],
                              student_number=post_data['contact1'],
                              parent_number=post_data['contact2'],
                              quota=quota,
                              ver=0)
        student_info.save()

        # Getting all filenames from the form
        file_names = [[*name.split(':')] for name in post_data.keys() if ":" in name]
        clean_names = {}
        for name in file_names:
            if name[0] in clean_names:
                clean_names[name[0]].append(name[1])
            else:
                clean_names[name[0]] = [name[1]]
        
        # Saving the file data
        for file in clean_names:
            doc = Document.objects.get(name = file)

            # Getting the info from post request
            original = post_data[file+":original"] == 'on'
            photo_copy = post_data[file+":copy"] == 'on'
            count = int(post_data[file+":count"])
            
            Record(student=student, document=doc,
                    original=original,
                    photocopy=photo_copy,
                    count=count,
                    date=datetime.strptime(post_data["date"], "%d/%m/%Y"),
                    ver=0).save()

        return redirect('next_page', receipt_no=student.admission_no)
    else:

        file_names= [document.name for document in Document.objects.all()]

        return render(request, "index.html", {"file_names": file_names})


def edit(request, admission_no):

    student = get_object_or_404(Student, admission_no=admission_no)
    if request.method == "POST":

        post_data = request.POST

        for data in post_data:
            print(type(post_data[data]), data, post_data[data])

        quota = post_data['quota'] == 'govt'
        
        # Saving the student info
        student.name=post_data['name_stu'],
        student.parent_name=post_data['name_prnt'],
        student.department=post_data['dept'],
        student.student_number=post_data['contact1'],
        student.parent_number=post_data['contact2'],
        student.quota=quota
        student.submit_count += 1
        student.save()

        # Getting all filenames from the form
        file_names = [[*name.split(':')] for name in post_data.keys() if ":" in name]
        clean_names = {}
        for name in file_names:
            if name[0] in clean_names:
                clean_names[name[0]].append(name[1])
            else:
                clean_names[name[0]] = [name[1]]
        
        # Saving the file data
        for file in clean_names:
            doc = Document.objects.get(name = file)

            # Getting the info from post request
            original = post_data[file+":original"] == 'on'
            photo_copy = post_data[file+":copy"] == 'on'
            count = int(post_data[file+":count"])
            
            Record(student=student, document=doc,
                    original=original,
                    photocopy=photo_copy,
                    count=count,
                    date=datetime.strptime(post_data["date"], "%d/%m/%Y"),
                    ver=student.submit_count).save()

        return redirect('next_page', receipt_no=student.recipt_no)
    else:
        records = student.record_set.filter(ver=student.submit_count)
        departments = ["CSE", "ECE", "CSBS", "AI&DS", "MECH", "IT"]
        return render(request, "edit.html", {"student": student, 'records': records, 'depts': departments})


def view(request, admission_no):
    student = get_object_or_404(Student, admission_no=admission_no)
    if 'version' in request.GET:
        version = int(request.GET.dict()["version"])
    else:
        version = student.version_count
    version = get_object_or_404(Version, version_count=version)
    info = get_object_or_404(StudentInfo, student=student, ver=version.stud_ver)
    records = Record.objects.filter(student=student, ver=version.docs_ver)
    version_values = [i + 1 for i in range(-1, student.version_count)]
    return render(request, "next-page.html", {"student": info, "records": records, "admission_no": admission_no, "versions": version_values, "cur_ver": version.version_count})