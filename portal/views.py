from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Record, Document, Student
from datetime import datetime


def home(request):
    if request.method == "POST":
        print(request.POST)
        post_data = request.POST

        # Saving the student info
        student = Student(name=post_data['name_stu'],
                          recipt_no=post_data['receipt'],
                          parent_name=post_data['name_prnt'],
                          department=post_data['dept'],
                          student_number=post_data['contact1'],
                          parent_number=post_data['contact2'])
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
                    date=datetime.strptime(post_data["date"], "%d/%m/%Y")).save()

        return HttpResponse("success")
    else:

        file_names= [document.name for document in Document.objects.all()]

        return render(request, "index.html", {"file_names": file_names})
