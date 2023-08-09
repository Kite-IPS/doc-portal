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



class StaffDashboard(View):

    def get(self, request):
        
        file_names= [document.name for document in Document.objects.all()]
        return render(request, "index.html", {"file_names": file_names})

    def post(self, request):

        self.parse_post_data(request)
        
        try:
            self.add_student()
        except ValueError:
            return HttpResponse("A Student with given id already exists!")
        
        return redirect("add")
    
    @staticmethod
    def doc_to_dict(doc):
        return {doc.name : {"original": doc.original, "copy": doc.copy, "count": doc.count}}
    
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

    @staticmethod
    def is_doc_modified(server_doc, request_doc):
        pass

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

    def parse_request(self, request):
        
        pass

    def lock_document(self):
        
        # Locking the student entry
        self.student.lock = True
        self.student.save()

    def is_locked(self):

        return self.student.lock

    def parse_post_data(self, request):

        # Getting the student admission number
        self.admission_no = request.POST.get("receipt")
 
        # Getting the student data from post
        self.student_info = {
            "student_name": request.POST.get("name_stu"),
            "parent_name": request.POST.get("name_prnt"),
            "dept": request.POST.get("dept"),
            "student_num": request.POST.get("contact1"),
            "parent_num": request.POST.get("contact2"),
            "email": request.POST.get("email"),
            "quota": request.POST.get("quota") == 'govt',
        }

        self.docs_info = {}

        # Looping through all the available docs and getting the data
        file_names = {name.split(':')[0] for name in request.POST.keys() if ":" in name}
        
        for name in file_names:
            self.docs_info[name] = {"original": request.POST.get(f"{name}:original") == 'on',
                                      "copy": request.POST.get(f"{name}:copy") == 'on',
                                      "count": int(request.POST.get(f"{name}:count"))}


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
