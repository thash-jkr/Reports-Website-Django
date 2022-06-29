from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Sale
from .forms import SalesSearchForm

# Create your views here.
def home(request):
    form = SalesSearchForm(request.POST or None)

    if request.method == "POST":
        date_from = request.POST.get("date_from")
        date_to = request.POST.get("date_to")
        chart_type = request.POST.get("chart_type")
        print(date_from, date_to, chart_type, end=" :)")

    hello = "Hello World!"
    context = {
        "hello": hello,
        "form": form
    }
    return render(request, "sales/home.html", context)


class SalesListView(ListView):
    model = Sale
    template_name = "sales/main.html"
    context_object_name = "objects"


class SalesDetailView(DetailView):
    model = Sale
    template_name = "sales/detail.html"
