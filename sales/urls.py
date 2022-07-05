from django.urls import path

from . import views

app_name = "sales"

urlpatterns = [
    path('', views.home, name="home"),
    path('from-file/', views.UploadTemplateView.as_view(), name="from_file"),
    path('upload/', views.csv_upload_view, name="csv_upload"),
    path('sales/', views.SalesListView.as_view(), name="list"),
    path('sales/<int:pk>/', views.SalesDetailView.as_view(), name="detail")
]