from django.urls import path

from . import views

app_name = "reports"

urlpatterns = [
    path('', views.ReportListView.as_view(), name="list"),
    path('save/', views.createReport, name="create"),
    path('pdf/', views.render_pdf_view, name="pdf"),
    path('<int:pk>/', views.ReportDetailView.as_view(), name="detail")
]