from django.urls import path
from .import views

urlpatterns = [
    path("", views.home, name='home'),
    path("edit/<receipt_no>", views.edit, name="edit"),
    path("next/<receipt_no>", views.next_page, name="next_page")
]