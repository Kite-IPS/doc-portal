from django.urls import path
from .import views

urlpatterns = [
    path("", views.home, name='home'),
    path("next/<receipt_no>", views.next_page, name="next_page")
]