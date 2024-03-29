from django.http import Http404
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from jmespath import search
from . import models, forms
from components.search_filter import search_filter


class LoggedInOnlyView(LoginRequiredMixin):
    login_url = reverse_lazy('users:login')

class HouseLeaseCustomerList(LoggedInOnlyView, ListView):
    model = models.HouseLeaseCustomer
    context_object_name = 'lists'
    template_name = 'customers/houselease/houselease_list.html'


class HouseLeaseCustomerDeatil(LoggedInOnlyView, DetailView):
    model = models.HouseLeaseCustomer
    template_name = 'customers/detail_total.html'

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.realtor.pk != self.request.user.pk:
            raise Http404()
        return room


class HouseLeaseCustomerCreating(LoggedInOnlyView, CreateView):
    form_class = forms.HouseLeaseCustomerForm
    template_name = 'customers/creating_total.html'

    def form_valid(self, form):
        book = form.save()
        book.realtor = self.request.user
        book.save()
        return redirect(reverse("customers:house-lease-customer-detail", kwargs={"pk":book.pk}))


class HouseLeaseCustomerUpdate(LoggedInOnlyView, UpdateView):
    model = models.HouseLeaseCustomer
    form_class = forms.HouseLeaseCustomerForm
    template_name = 'customers/creating_total.html'

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.realtor.pk != self.request.user.pk:
            raise Http404()
        return room

    def form_valid(self, form):
        book = form.save()
        book.realtor = self.request.user
        book.save()
        return redirect(reverse("customers:house-lease-customer-detail", kwargs={"pk":book.pk}))


def houselease_customer_search(request):
    filter_args = search_filter(request)
    lists = models.HouseLeaseCustomer.objects.filter(
        **filter_args)
    return render(request, "customers/houselease/houselease_search.html", {**filter_args, "lists": lists})


@login_required
def houselease_customer_delete(request, pk):
    houselease_customer = models.HouseLeaseCustomer.objects.filter(pk=pk)
    houselease_customer.delete()
    return redirect(reverse("customers:house-lease-customer-list"))

""""""
class ApartmentLeaseCustomerList(LoggedInOnlyView, ListView):
    model = models.ApartmentLeaseCustomer
    context_object_name = 'lists'
    template_name = 'customers/apartmentlease/apartmentlease_list.html'


class ApartmentLeaseCustomerDeatil(LoggedInOnlyView, DetailView):
    model = models.ApartmentLeaseCustomer
    template_name = 'customers/detail_total.html'

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.realtor.pk != self.request.user.pk:
            raise Http404()
        return room


class ApartmentLeaseCustomerCreating(LoggedInOnlyView, CreateView):
    form_class = forms.ApartmentLeaseCustomerForm
    template_name = 'customers/creating_total.html'

    def form_valid(self, form):
        book = form.save()
        book.realtor = self.request.user
        book.save()
        return redirect(reverse("customers:apartment-lease-customer-detail", kwargs={"pk":book.pk}))


class ApartmentLeaseCustomerUpdate(LoggedInOnlyView, UpdateView):
    model = models.ApartmentLeaseCustomer
    form_class = forms.ApartmentLeaseCustomerForm
    template_name = 'customers/creating_total.html'

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.realtor.pk != self.request.user.pk:
            raise Http404()
        return room

    def form_valid(self, form):
        book = form.save()
        book.realtor = self.request.user
        book.save()
        return redirect(reverse("customers:apartment-lease-customer-detail", kwargs={"pk":book.pk}))


def apartmentlease_customer_search(request):
    filter_args = search_filter(request)
    lists = models.ApartmentLeaseCustomer.objects.filter(
        **filter_args)
    return render(request, "customers/apartmentlease/apartmentlease_search.html", {**filter_args, "lists": lists})


@login_required
def apartmentlease_customer_delete(request, pk):
    apartmentlease_customer = models.ApartmentLeaseCustomer.objects.filter(pk=pk)
    apartmentlease_customer.delete()
    return redirect(reverse("customers:apartment-lease-customer-list"))

""""""

class OfficetelLeaseCustomerList(LoggedInOnlyView, ListView):
    model = models.OfficetelLeaseCustomer
    context_object_name = 'lists'
    template_name = 'customers/officetellease/officetellease_list.html'


class OfficetelLeaseCustomerDeatil(LoggedInOnlyView, DetailView):
    model = models.OfficetelLeaseCustomer
    template_name = 'customers/detail_total.html'

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.realtor.pk != self.request.user.pk:
            raise Http404()
        return room


class OfficetelLeaseCustomerCreating(LoggedInOnlyView, CreateView):
    form_class = forms.OfficetelLeaseCustomerForm
    template_name = 'customers/creating_total.html'

    def form_valid(self, form):
        book = form.save()
        book.realtor = self.request.user
        book.save()
        return redirect(reverse("customers:officetel-lease-customer-detail", kwargs={"pk":book.pk}))


class OfficetelLeaseCustomerUpdate(LoggedInOnlyView, UpdateView):
    model = models.OfficetelLeaseCustomer
    form_class = forms.OfficetelLeaseCustomerForm
    template_name = 'customers/creating_total.html'

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.realtor.pk != self.request.user.pk:
            raise Http404()
        return room

    def form_valid(self, form):
        book = form.save()
        book.realtor = self.request.user
        book.save()
        return redirect(reverse("customers:officetel-lease-customer-detail", kwargs={"pk":book.pk}))


def officetellease_customer_search(request):
    filter_args = search_filter(request)
    lists = models.OfficetelLeaseCustomer.objects.filter(
        **filter_args)
    return render(request, "customers/officetellease/officetellease_search.html", {**filter_args, "lists": lists})


@login_required
def officetellease_customer_delete(request, pk):
    officetellease_customer = models.OfficetelLeaseCustomer.objects.filter(pk=pk)
    officetellease_customer.delete()
    return redirect(reverse("customers:officetel-lease-customer-list"))

"""below shoplease"""


class ShopLeaseCustomerList(LoggedInOnlyView, ListView):
    model = models.ShopLeaseCustomer
    context_object_name = 'lists'
    template_name = 'customers/shoplease/shoplease_list.html'


class ShopLeaseCustomerDeatil(LoggedInOnlyView, DetailView):
    model = models.ShopLeaseCustomer
    template_name = 'customers/detail_total.html'

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.realtor.pk != self.request.user.pk:
            raise Http404()
        return room


class ShopLeaseCustomerCreating(LoggedInOnlyView, CreateView):
    form_class = forms.ShopLeaseCustomerForm
    template_name = 'customers/creating_total.html'

    def form_valid(self, form):
        book = form.save()
        book.realtor = self.request.user
        book.save()
        return redirect(reverse("customers:shop-lease-customer-detail", kwargs={"pk":book.pk}))


class ShopLeaseCustomerUpdate(LoggedInOnlyView, UpdateView):
    model = models.ShopLeaseCustomer
    form_class = forms.ShopLeaseCustomerForm
    template_name = 'customers/creating_total.html'

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.realtor.pk != self.request.user.pk:
            raise Http404()
        return room

    def form_valid(self, form):
        book = form.save()
        book.realtor = self.request.user
        book.save()
        return redirect(reverse("customers:shop-lease-customer-detail", kwargs={"pk":book.pk}))


def shoplease_customer_search(request):
    filter_args = search_filter(request)
    lists = models.ShopLeaseCustomer.objects.filter(
        **filter_args)
    return render(request, "customers/shoplease/shoplease_search.html", {**filter_args, "lists": lists})


@login_required
def shoplease_customer_delete(request, pk):
    shoplease_customer = models.ShopLeaseCustomer.objects.filter(pk=pk)
    shoplease_customer.delete()
    return redirect(reverse("customers:shop-lease-customer-list"))


"""below housedealing"""

class HouseDealingCustomerList(LoggedInOnlyView, ListView):
    model = models.HouseDealingCustomer
    context_object_name = 'lists'
    template_name = 'customers/housedealing/housedealing_list.html'


class HouseDealingCustomerDeatil(LoggedInOnlyView, DetailView):
    model = models.HouseDealingCustomer
    template_name = 'customers/detail_total.html'

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.realtor.pk != self.request.user.pk:
            raise Http404()
        return room


class HouseDealingCustomerCreating(LoggedInOnlyView, CreateView):
    form_class = forms.HouseDealingCustomerForm
    template_name = 'customers/creating_total.html'

    def form_valid(self, form):
        book = form.save()
        book.realtor = self.request.user
        book.save()
        return redirect(reverse("customers:house-dealing-customer-detail", kwargs={"pk":book.pk}))


class HouseDealingCustomerUpdate(LoggedInOnlyView, UpdateView):
    model = models.HouseDealingCustomer
    form_class = forms.HouseDealingCustomerForm
    template_name = 'customers/creating_total.html'

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.realtor.pk != self.request.user.pk:
            raise Http404()
        return room

    def form_valid(self, form):
        book = form.save()
        book.realtor = self.request.user
        book.save()
        return redirect(reverse("customers:house-dealing-customer-detail", kwargs={"pk":book.pk}))


def housedealing_customer_search(request):
    filter_args = search_filter(request)
    lists = models.HouseDealingCustomer.objects.filter(
        **filter_args)
    return render(request, "customers/housedealing/housedealing_search.html", {**filter_args, "lists": lists})


@login_required
def housedealing_customer_delete(request, pk):
    housedealing_customer = models.HouseDealingCustomer.objects.filter(pk=pk)
    housedealing_customer.delete()
    return redirect(reverse("customers:house-dealing-customer-list"))

""""""

class ApartmentDealingCustomerList(LoggedInOnlyView, ListView):
    model = models.ApartmentDealingCustomer
    context_object_name = 'lists'
    template_name = 'customers/apartmentdealing/apartmentdealing_list.html'


class ApartmentDealingCustomerDeatil(LoggedInOnlyView, DetailView):
    model = models.ApartmentDealingCustomer
    template_name = 'customers/detail_total.html'

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.realtor.pk != self.request.user.pk:
            raise Http404()
        return room


class ApartmentDealingCustomerCreating(LoggedInOnlyView, CreateView):
    form_class = forms.ApartmentDealingCustomerForm
    template_name = 'customers/creating_total.html'

    def form_valid(self, form):
        book = form.save()
        book.realtor = self.request.user
        book.save()
        return redirect(reverse("customers:apartment-dealing-customer-detail", kwargs={"pk":book.pk}))


class ApartmentDealingCustomerUpdate(LoggedInOnlyView, UpdateView):
    model = models.ApartmentDealingCustomer
    form_class = forms.ApartmentDealingCustomerForm
    template_name = 'customers/creating_total.html'

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.realtor.pk != self.request.user.pk:
            raise Http404()
        return room

    def form_valid(self, form):
        book = form.save()
        book.realtor = self.request.user
        book.save()
        return redirect(reverse("customers:apartment-dealing-customer-detail", kwargs={"pk":book.pk}))


def apartmentdealing_customer_search(request):
    filter_args = search_filter(request)
    lists = models.ApartmentDealingCustomer.objects.filter(**filter_args)
    return render(request, "customers/apartmentdealing/apartmentdealing_search.html", {**filter_args, "lists": lists})


@login_required
def apartmentdealing_customer_delete(request, pk):
    apartmentdealing_customer = models.ApartmentDealingCustomer.objects.filter(pk=pk)
    apartmentdealing_customer.delete()
    return redirect(reverse("customers:apartment-dealing-customer-list"))

""""""

class OfficetelDealingCustomerList(LoggedInOnlyView, ListView):
    model = models.OfficetelDealingCustomer
    context_object_name = 'lists'
    template_name = 'customers/officeteldealing/officeteldealing_list.html'


class OfficetelDealingCustomerDeatil(LoggedInOnlyView, DetailView):
    model = models.OfficetelDealingCustomer
    template_name = 'customers/detail_total.html'

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.realtor.pk != self.request.user.pk:
            raise Http404()
        return room


class OfficetelDealingCustomerCreating(LoggedInOnlyView, CreateView):
    form_class = forms.OfficetelDealingCustomerForm
    template_name = 'customers/creating_total.html'

    def form_valid(self, form):
        book = form.save()
        book.realtor = self.request.user
        book.save()
        return redirect(reverse("customers:officetel-dealing-customer-detail", kwargs={"pk":book.pk}))


class OfficetelDealingCustomerUpdate(LoggedInOnlyView, UpdateView):
    model = models.OfficetelDealingCustomer
    form_class = forms.OfficetelDealingCustomerForm
    template_name = 'customers/creating_total.html'

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.realtor.pk != self.request.user.pk:
            raise Http404()
        return room

    def form_valid(self, form):
        book = form.save()
        book.realtor = self.request.user
        book.save()
        return redirect(reverse("customers:officetel-dealing-customer-detail", kwargs={"pk":book.pk}))


def officeteldealing_customer_search(request):
    filter_args = search_filter(request)
    lists = models.OfficetelDealingCustomer.objects.filter(
        **filter_args)
    return render(request, "customers/officeteldealing/officeteldealing_search.html", {**filter_args, "lists": lists})


@login_required
def officeteldealing_customer_delete(request, pk):
    officeteldealing_customer = models.OfficetelDealingCustomer.objects.filter(pk=pk)
    officeteldealing_customer.delete()
    return redirect(reverse("customers:officetel-dealing-customer-list"))

""""""
class ShopDealingCustomerList(LoggedInOnlyView, ListView):
    model = models.ShopDealingCustomer
    context_object_name = 'lists'
    template_name = 'customers/shopdealing/shopdealing_list.html'


class ShopDealingCustomerDeatil(LoggedInOnlyView, DetailView):
    model = models.ShopDealingCustomer
    template_name = 'customers/detail_total.html'

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.realtor.pk != self.request.user.pk:
            raise Http404()
        return room


class ShopDealingCustomerCreating(LoggedInOnlyView, CreateView):
    form_class = forms.ShopDealingCustomerForm
    template_name = 'customers/creating_total.html'

    def form_valid(self, form):
        book = form.save()
        book.realtor = self.request.user
        book.save()
        return redirect(reverse("customers:shop-dealing-customer-detail", kwargs={"pk":book.pk}))


class ShopDealingCustomerUpdate(LoggedInOnlyView, UpdateView):
    model = models.ShopDealingCustomer
    form_class = forms.ShopDealingCustomerForm
    template_name = 'customers/creating_total.html'

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.realtor.pk != self.request.user.pk:
            raise Http404()
        return room

    def form_valid(self, form):
        book = form.save()
        book.realtor = self.request.user
        book.save()
        return redirect(reverse("customers:shop-dealing-customer-detail", kwargs={"pk":book.pk}))


def shopdealing_customer_search(request):
    filter_args = search_filter(request)
    lists = models.ShopDealingCustomer.objects.filter(
        **filter_args)
    return render(request, "customers/shopdealing/shopdealing_search.html", {**filter_args, "lists": lists})


@login_required
def shopdealing_customer_delete(request, pk):
    shopdealing_customer = models.ShopDealingCustomer.objects.filter(pk=pk)
    shopdealing_customer.delete()
    return redirect(reverse("customers:shop-dealing-customer-list"))

"""below buildingdealing"""


class BuildingDealingCustomerList(LoggedInOnlyView, ListView):
    model = models.BuildingDealingCustomer
    context_object_name = 'lists'
    template_name = 'customers/buildingdealing/buildingdealing_list.html'


class BuildingDealingCustomerDeatil(LoggedInOnlyView, DetailView):
    model = models.BuildingDealingCustomer
    template_name = 'customers/detail_total.html'

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.realtor.pk != self.request.user.pk:
            raise Http404()
        return room


class BuildingDealingCustomerCreating(LoggedInOnlyView, CreateView):
    form_class = forms.BuildingDealingCustomerForm
    template_name = 'customers/creating_total.html'

    def form_valid(self, form):
        book = form.save()
        book.realtor = self.request.user
        if book.land_m2 is None:
            book.land_m2 = 0
        book.save()
        return redirect(reverse("customers:building-dealing-customer-detail", kwargs={"pk":book.pk}))


class BuildingDealingCustomerUpdate(LoggedInOnlyView, UpdateView):
    model = models.BuildingDealingCustomer
    form_class = forms.BuildingDealingCustomerForm
    template_name = 'customers/creating_total.html'

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.realtor.pk != self.request.user.pk:
            raise Http404()
        return room

    def form_valid(self, form):
        book = form.save()
        book.realtor = self.request.user
        if book.land_m2 is None:
            book.land_m2 = 0
        book.save()
        return redirect(reverse("customers:building-dealing-customer-detail", kwargs={"pk":book.pk}))


def buildingdealing_customer_search(request):
    filter_args = search_filter(request)
    lists = models.BuildingDealingCustomer.objects.filter(**filter_args)
    return render(request, "customers/buildingdealing/buildingdealing_search.html", {**filter_args, "lists": lists})


@login_required
def buildingdealing_customer_delete(request, pk):
    buildingdealing_customer = models.BuildingDealingCustomer.objects.filter(
        pk=pk)
    buildingdealing_customer.delete()
    return redirect(reverse("customers:building-dealing-customer-list"))
