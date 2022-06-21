from django.shortcuts import render
from django.views.generic import ListView

from .models import Sale

# Create your views here.
def home(request):
    context = {}
    return render(request, "sales/home.html", context)


class SalesListView(ListView):
    model = Sale
    template_name = "sales/main.html"
    context_object_name = "objects"
