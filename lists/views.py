from django.http import HttpResponse
from django.shortcuts import render


def home_page(request):
    template_name = '<html><title>To-Do lists</title></html>'
    # return render(request=request, template_name=template_name)
    return HttpResponse(template_name)
