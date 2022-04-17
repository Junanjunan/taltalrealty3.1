from datetime import timedelta, date
from django.http import Http404
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from . import models, forms


class LoggedInOnlyView(LoginRequiredMixin):
    login_url = reverse_lazy('users:login')

class ContractsList(LoggedInOnlyView, ListView):
    model = models.ContractBase
    context_object_name = "lists"


class ContractCreating(LoggedInOnlyView, CreateView):
    form_class = forms.ContractForm
    template_name = 'contracts/contract_creating.html'

    def form_valid(self, form):
        book = form.save()
        book.realtor = self.request.user
        book.due_days = book.last_day - date.today()
        if book.types != "Deal":
            book.price = 0
        book.save()
        return redirect(reverse("contracts:detail", kwargs={"pk":book.pk}))


class ContractUpdate(LoggedInOnlyView, UpdateView):
    model = models.ContractBase
    form_class = forms.ContractForm
    template_name = 'contracts/contract_creating.html'

    def get_object(self, queryset=None):
        contract = super().get_object(queryset=queryset)
        if contract.realtor.pk != self.request.user.pk:
            raise Http404()
        return contract

    def form_valid(self, form):
        contract = form.save()
        contract.realtor = self.request.user
        contract.save()
        return redirect(reverse("contracts:detail", kwargs={"pk":contract.pk}))


class ContractDetail(LoggedInOnlyView, DetailView):
    model = models.ContractBase
    template_name = 'contracts/contract_detail.html'

    def get_object(self, queryset=None):
        contract = super().get_object(queryset=queryset)
        if contract.realtor.pk != self.request.user.pk:
            raise Http404()
        return contract


@login_required
def contract_delete(request, pk):
    contract = models.ContractBase.objects.filter(pk=pk).delete()
    return redirect(reverse("contracts:list"))