from django.urls import path
from .import views

urlpatterns = [
    path("dashboard", views.home, name='dashboard'),
    path("", views.add, name='add'),
    path("edit/<admission_no>", views.edit, name="edit"),
    path("view/<admission_no>", views.view, name="view"),
    path("pdf/<admission_no>", views.pdf_download, name="pdf")
]