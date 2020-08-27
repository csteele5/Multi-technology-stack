from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template

# from schedule.models import Sprint

def home_page(request):
    # my_title = "Agile Sprint List"
    # qs = Sprint.objects.all()[:10]
    # context = {"title": "Welcome to the Sprint Planner", 'sprint_list': qs}
    context = {}
    return render(request, "home.html", context)