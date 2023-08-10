from django.urls import path
from .import views

urlpatterns = [
    path("dashboard", views.home, name='dashboard'),
    path("", views.AddNewStudent.as_view(), name='add'),
    path("", views.EditAndViewStudents.as_view(), name='edit'),
    path("pdf/<admission_no>", views.pdf_download, name="pdf")
]