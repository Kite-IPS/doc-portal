from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import views as auth_views
from django.utils import timezone
from django.db import IntegrityError
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from .utils import *
from .models import *
from .forms import AuthForm


class LoginView(auth_views.LoginView):
    form_class = AuthForm


def home(request):
    return render(request, "dashboard.html")



class AddNewStudent(View):

    def get(self, request):
        
        file_names= [document.name for document in Document.objects.all()]
        return render(request, "add.html", {"file_names": file_names, "date": timezone.localdate()})

    def post(self, request):

        self.parse_post_data(request)
        
        try:
            self.add_student()
        except ValueError:
            return HttpResponse("A Student with given id already exists!")
        
        return redirect("add")

    def add_student(self):

        # Checking if a student with given id already exist
        if self.check_num(self.admission_no):
            raise ValueError
        
        # Create a new student
        student = Student(admission_no=self.admission_no,
                          version_count=0,
                          lock = False)
        student.save()
        
        # Create related versions
        version = Version(student=student,
                          version_count=0,
                          docs_ver=0,
                          stud_ver=0)
        version.save()

        # Creating Student info version
        info = StudentInfo(
            student = student,
            name = self.student_info['student_name'],
            student_number = self.student_info['student_num'],
            parent_name = self.student_info["parent_name"],
            parent_number = self.student_info['parent_num'],
            email = self.student_info['email'],
            department = self.student_info['dept'],
            quota = self.student_info['quota'],
            ver = 0
        )

        info.save()

        # Saving the documents
        docs_list = Document.objects.all()
        for doc, val in self.docs_info.items():
            Record(ver=0,
                   date=timezone.localdate(),
                   student=student,
                   original=val["original"],
                   photocopy=val["copy"],
                   count=val["count"],
                   document=docs_list.get(name=doc)).save()

    def check_num(self, admission_no):

        return Student.objects.filter(admission_no=admission_no).exists()

    def lock_document(self):
        
        # Locking the student entry
        self.student.lock = True
        self.student.save()

    def parse_post_data(self, request):

        post_data = request.POST.dict()
        print(post_data)

        # Getting the student admission number
        self.admission_no = post_data.get("receipt")
 
        # Getting the student data from post
        self.student_info = {
            "student_name": post_data.get("name_stu"),
            "parent_name": post_data.get("name_prnt"),
            "dept": post_data.get("dept"),
            "student_num": post_data.get("contact1"),
            "parent_num": post_data.get("contact2"),
            "email": post_data.get("email"),
            "quota": post_data.get("quota") == 'govt',
        }

        self.docs_info = {}

        # Looping through all the available docs and getting the data
        file_names = {name.split(':')[0] for name in post_data.keys() if ":" in name}
        
        for name in file_names:
            count_str = post_data.get(f"{name}:count")
            count = int(count_str) if count_str.isdigit() else 0
            self.docs_info[name] = {"original": post_data.get(f"{name}:original") == 'on',
                                      "copy": post_data.get(f"{name}:copy") == 'on',
                                      "count": count}


class EditAndViewStudents(AddNewStudent):


    def get(self, request, admission_no):

        self.admission_no = admission_no
        self.student = get_object_or_404(Student, admission_no=self.admission_no)
        
        # Checking if a version is given in route
        if 'version' in request.GET:
            version = int(request.GET.dict()["version"])
        else:
            version = self.student.version_count
        
        view_context = self.get_student_history(version)
        edit_context = self.get_student_history(self.student.version_count)

        return render(request, "view_and_edit.html", {"edit_context":edit_context, "view_context": view_context})
    
    def get_student_history(self, version_num):

        version = get_object_or_404(Version, version_count=version_num, student=self.student)
        info = get_object_or_404(StudentInfo, student=self.student, ver=version.stud_ver)
        records = Record.objects.filter(student=self.student, ver=version.docs_ver)
        version_values = [i + 1 for i in range(0, self.student.version_count+1)]

        return {"student": info, "records": records, "admission_no": self.admission_no, "versions": version_values, "cur_ver": version.version_count}


    def post(self, request, admission_no):
        
        parsed_data = self.parse_post_data(request)
        print(parsed_data)

        return HttpResponse("saved")

    @staticmethod
    def doc_to_dict(doc):
        return {doc.name : {"original": doc.original, "copy": doc.copy, "count": doc.count}}
    
    @staticmethod
    def is_doc_modified(server_doc, request_doc):
        pass
        
    @staticmethod
    def student_info_to_dict(student_info):

        return {
        "student_name":student_info.name,
        "student_num":student_info.student_number,
        "parent_name":student_info.parent_name,
        "parent_num":student_info.parent_number,
        "email":student_info.email,
        "dept":student_info.department,
        "quota":student_info.quota,
        }

    def is_locked(self):

        return self.student.lock


def pdf_download(request, admission_no):

    template_path = 'print.html'
    context = get_student_info(request, admission_no)
    
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
