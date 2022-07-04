from django.urls import path

from . import views

app_name = "reports"

urlpatterns = [
    path('save/', views.createReport, name="create")
]