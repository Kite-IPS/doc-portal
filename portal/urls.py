from django.urls import path
from .import views

urlpatterns = [
    path("", views.home, name='home'),
    path("edit/<admission_no>", views.edit, name="edit"),
    path("view/<admission_no>", views.view, name="view")
]