from django.shortcuts import render

from .models import Profile
from .forms import ProfileForm

# Create your views here.
def profile_view(request):
    context = {}
    return render(request, "profiles/main.html", context)
