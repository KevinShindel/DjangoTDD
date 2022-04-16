from django.shortcuts import render, redirect
from django.views.generic import FormView, CreateView, DetailView

from accounts.models import User
from lists.forms import ExistingListItemForm, NewListForm, ItemForm
from lists.models import List


class HomePageView(FormView):
    template_name = 'lists/home.html'
    form_class = ItemForm


class ViewAndAddToList(DetailView, CreateView):
    model = List
    template_name = 'lists/list.html'
    form_class = ExistingListItemForm

    def get_form(self, form_class=None):
        self.object = self.get_object()
        return self.form_class(for_list=self.object, data=self.request.POST)


def new_list_isolated(request):
    ''' новый список 2'''
    template_name = 'lists/home.html'
    form = NewListForm(data=request.POST)
    if form.is_valid():
        list_ = form.save(owner=request.user)
        return redirect(list_)
    return render(request=request, template_name=template_name, context={'form': form})


class NewListView(CreateView, HomePageView):

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user if request.user.is_authenticated else None
        return super(NewListView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        list_ = List.objects.create(owner=self.user)
        form.save(for_list=list_)
        return redirect(list_)


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
