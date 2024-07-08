from django.shortcuts import render
from.models import Report
from django.contrib.auth.models import User
from django.db.models import Q
# from django.http import HttpResponse
from django .contrib.auth.decorators import login_required



@login_required
def report(request):

    myreport=Report.objects.all()
    context={
        'reports':myreport,
        'title' : 'Report',
    }

    return render(request, 'blog/report.html',context)

def home(request):
    return render(request, 'blog/home.html',{'title':'Home'})
