from django.shortcuts import render, redirect

from lists.forms import ItemForm, ExistingListItemForm
from lists.models import List


def new_list(request):
    ''' новый список '''
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request=request,
                      template_name='lists/home.html',
                      context={'form': form})


def home_page(request):
    template_name = 'lists/home.html'
    return render(request=request, template_name=template_name, context={'form': ItemForm()})


def view_list(request, list_id):
    ''' представление списка '''
    template_name = 'lists/list.html'
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(data=request.POST, for_list=list_)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request=request, template_name=template_name,
                  context={'list': list_, 'form': form})

def my_lists(request, email):
    template_name = 'lists/my_lists.html'
    return render(request=request, template_name=template_name)