from django.urls import path

from . import views

app_name = "sales"

urlpatterns = [
    path('', views.home, name="home"),
    path('list/', views.SalesListView.as_view(), name="list")
]