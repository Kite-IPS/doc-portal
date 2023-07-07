from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("summary_page", summary_page, name="summary")
]