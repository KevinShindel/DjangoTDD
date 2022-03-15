from django.shortcuts import render, redirect

from accounts.models import User
from lists.forms import ItemForm, ExistingListItemForm, NewListForm
from lists.models import List


def new_list_isolated(request):
    ''' новый список 2'''
    template_name = 'lists/home.html'
    form = NewListForm(data=request.POST)
    if form.is_valid():
        list_ = form.save(owner=request.user)
        return redirect(list_)
    return render(request=request, template_name=template_name, context={'form': form})


def new_list(request):
    ''' новый список '''

    form = NewListForm(data=request.POST)
    if form.is_valid():
        list_ = form.save(owner=request.user)
        return redirect(list_)
    return render(request=request, template_name='lists/home.html', context={'form': form})


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
    owner, _ = User.objects.get_or_create(email=email)
    return render(request=request, template_name=template_name, context={'owner': owner})
