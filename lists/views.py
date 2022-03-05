from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from lists.models import Item, List


def new_list(request):
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request=request, template_name='lists/home.html', context={'error': error})
    return redirect(to=f'/lists/{list_.id}/')


def home_page(request):
    template_name = 'lists/home.html'
    return render(request=request, template_name=template_name)


def view_list(request, list_id):
    template_name = 'lists/list.html'
    return render(request=request, template_name=template_name, context={'list': List.objects.get(id=list_id)})


def add_item(request, list_id):
    Item.objects.create(text=request.POST['item_text'], list_id=list_id)
    return redirect(to=f'/lists/{list_id}/')
