from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader



def index(request):
    template = loader.get_template("result_Home.html")
    # results = VisaGetlist.objects.all()
    context = {'user': 'arun'}
    rendered_template = template.render(context)
    return HttpResponse(rendered_template)