from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from v1.db.models import Currency

from .forms import *

from django.forms import formset_factory
from django.forms import modelformset_factory
from django.db import transaction, IntegrityError


@login_required
@permission_required(['db.add.currency'], raise_exception=True)
def create_currency(request):
    context = {}
    CurrencyFormset = modelformset_factory(Currency, form=CurrencyForm)
    formset = CurrencyFormset(
        request.POST or None, queryset=Currency.objects.none(), prefix='currency')

    if request.method == 'POST':
        if formset.is_valid():
            try:
                with transaction.atomic():
                    for currency in formset:
                        currency.save()
            except IntegrityError:
                print("Error Encountered")
            return redirect('web:currency_list')
        else:
            print('='*10, formset.errors)
            messages.error(request, formset.errors)

    context['title'] = 'Add Currency'
    context['formset'] = formset
    return render(request, 'admin/other/create_currency.html', context)


class CurrencyList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('db.view_currency')
    model = Currency
    context_object_name = 'currencies'
    template_name = 'admin/other/currency_list.html'
    # paginate_by = 10
