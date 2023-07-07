from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Record,Document,Student

def home (request):
    if request.method=="POST":
        print("requeest")
        print(request.POST)
        date = request.POST['date']
        student = request.POST['student']
        original = request.POST.GET('orginal',False)
        photocopy = request.POST.GET('photocopy',False)
        count = request.POST['count']
        document_id = request.POST['document']
        '''
        # create a new record 
        for data_item in data:
            # Extract data from data_item
            name = data_item['name']
            receipt_no = data_item['receipt_no']
            department = data_item['department']
            student_number = data_item['student_number']
            parent_name = data_item['parent_name']
            documents = data_item['documents']
            
            
            student = Student(
                name=name,
                receipt_no=receipt_no,
                department=department,
                student_number=student_number,
                parent_name=parent_name,
                parent_number=parent_number
            )
            student.save()
            
            for Document in data:
                document= Document.objects.get(id=document_id)
                record = Record(
                    date=date,
                    student=student,
                    original=original,
                    photocopy=photocopy,
                    count=count,
                    document=document,
                )
                record.save()

                return redirect('record_list')
    '''
    else:
        records = Record.objects.all()
        return render(request, 'index.html', {'records': records})





