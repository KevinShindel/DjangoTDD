from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from lists.models import Item


def home_page(request):
    template_name = 'lists/home.html'
    if request.method == 'POST':
        new_item_text = request.POST.get('item_text', '')
        Item.objects.create(text=new_item_text)
        return redirect('/lists/один-единственный-список-в-мире/')
    context = {'items': Item.objects.all()}
    return render(request=request, template_name=template_name, context=context)


def view_list(request):
    template_name = 'lists/list.html'
    return render(request=request, template_name=template_name, context={'items': Item.objects.all()})


# class HomePageView(TemplateView):
#     template_name = 'lists/home.html'
