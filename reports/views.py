from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import ListView, DetailView

from profiles.models import Profile
from .models import Report
from .utils import GetReportImage
from .forms import ReportForm

# Create your views here.
class ReportListView(ListView):
    model = Report
    template_name = "reports/main.html"


class ReportDetailView(DetailView):
    model = Report
    template_name = "reports/detail.html"


def createReport(request):
    form = ReportForm(request.POST or None)
    if request.method == "POST":
        # name = request.POST.get("name")
        # remarks = request.POST.get("remarks")
        image = request.POST.get("image")
        image = GetReportImage(image)
        author = Profile.objects.get(user=request.user)
        # Report.objects.create(name=name, remarks=remarks, image=image, author=author)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.image = image
            instance.author = author
            instance.save()

        return JsonResponse({"msg": "send"})
    return JsonResponse({})
