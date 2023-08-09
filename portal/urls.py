from django.urls import path
from .import views

urlpatterns = [
    path("dashboard", views.home, name='dashboard'),
    path("", views.StaffDashboard.as_view(), name='add'),
    path("pdf/<admission_no>", views.pdf_download, name="pdf")
]