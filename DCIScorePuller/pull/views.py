from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(request):
    return render(request, 'pull/home.html')

def about(request):
    return render(request, 'pull/about.html')

def welcome(request):    
    if not request.user.is_authenticated:
        return render(request=request, template_name='pull/welcome.html')
    else:
        return home(request)