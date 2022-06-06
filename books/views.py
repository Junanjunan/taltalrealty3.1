from django import forms as django_forms
from django.http import Http404
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import View, ListView, CreateView, DetailView, UpdateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from . import models, forms
from django.utils import timezone


class LoggedInOnlyView(LoginRequiredMixin):
    login_url = reverse_lazy('users:login')


class BnCView(LoggedInOnlyView, ListView):
    model = models.RoomLease
    template_name = 'partials/bnc.html'


class RoomLeaseList(LoggedInOnlyView, ListView):
    model = models.RoomLease
    context_object_name = 'lists'
    template_name = 'books/roomlease/roomlease_list.html'
    


class RoomLeaseDetail(LoggedInOnlyView, DetailView):
    model = models.RoomLease
    # template_name = 'books/roomlease/roomlease_detail.html'
    template_name = 'books/detail_total.html'

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.realtor.pk != self.request.user.pk:
            raise Http404()
        return room


class RoomLeaseCreating(LoggedInOnlyView, CreateView):
    form_class = forms.RoomLeaseForm
    # template_name = 'books/roomlease/roomlease_creating.html'
    template_name = 'books/creating_total.html'

    def form_valid(self, form):
        book = form.save()
        book.realtor = self.request.user
        if book.bath is None:
            book.bath = 0
        if book.management_fee is None:
            book.management_fee = 0
        if book.total_area_m2 is None:
            book.total_area_m2 = 0
        if book.owner_phone is None:
            book.owner_phone = "-"
        if book.tenant_phone is None:
            book.tenant_phone = "-"
        book.save()
        return redirect(reverse("books:room-lease-detail", kwargs={"pk":book.pk}))
    # def get_success_url(self):
    #     return reverse("books:room-lease-list")   # 위 아래 둘 다 가능


class RoomLeaseUpdate(LoggedInOnlyView, UpdateView):
    model = models.RoomLease
    form_class = forms.RoomLeaseForm
    # template_name = "books/roomlease/roomlease_update.html"
    template_name = 'books/creating_total.html'
    

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.realtor.pk != self.request.user.pk:
            raise Http404()
        return room

    def form_valid(self, form):
        book = form.save()
        book.realtor = self.request.user
        if book.bath is None:
            book.bath = 0
        if book.management_fee is None:
            book.management_fee = 0
        if book.total_area_m2 is None:
            book.total_area_m2 = 0
        if book.owner_phone is None:
            book.owner_phone = "-"
        if book.tenant_phone is None:
            book.tenant_phone = "-"
        book.save()
        return redirect(reverse("books:room-lease-detail", kwargs={"pk":book.pk}))


def roomlease_search(request):

    address = request.GET.get("address")
    try:
        deposit = int(request.GET.get("deposit", 0))
    except:
        messages.error(request, "최대 보증금을 입력해주세요")
        return redirect(reverse("books:room-lease-list"))
    try:
        month_fee = int(request.GET.get("month_fee", 0))
    except:
        messages.error(request, "최대 월세를 입력해주세요")
        return redirect(reverse("books:room-lease-list"))
    try:
        area_m2 = int(request.GET.get("area_m2", 0))
    except:
        messages.error(request, "최소 면적을 입력해주세요")
        return redirect(reverse("books:room-lease-list"))
    room = request.GET.get("room", 0)
    parking = request.GET.get("parking")
    elevator = request.GET.get("elevator")
    loan = request.GET.get("loan")
    empty = request.GET.get("empty")
    not_finished = request.GET.get("not_finished")
    naver = request.GET.get("naver")
    dabang = request.GET.get("dabang")
    zicbang = request.GET.get("zicbang")
    peterpan = request.GET.get("peterpan")
    description = request.GET.get("description")

    filter_args = {}
    filter_args["address__contains"] = address
    filter_args["description__contains"] = description
    filter_args["deposit__lte"] = deposit
    filter_args["month_fee__lte"] = month_fee
    filter_args["area_m2__gte"] = area_m2
    filter_args["room__contains"] = room
    if parking == "on":
        filter_args["parking"] = True
    if elevator == "on":
        filter_args["elevator"] = True
    if loan == "on":
        filter_args["loan"] = True
    if empty == "on":
        filter_args["empty"] = True
    if not_finished == "on":
        filter_args["not_finished"] = True
    if naver == "on":
        filter_args["naver"] = True
    if dabang == "on":
        filter_args["dabang"] = True
    if zicbang == "on":
        filter_args["zicbang"] = True
    if peterpan == "on":
        filter_args["peterpan"] = True
    lists = models.RoomLease.objects.filter(**filter_args)
    return render(request, "books/roomlease/roomlease_search.html", {**filter_args, "lists": lists})


@login_required
def roomlease_delete(request, pk):
    room = models.RoomLease.objects.filter(pk=pk).delete()
    return redirect(reverse("books:room-lease-list"))


""""""
class ApartmentLeaseList(LoggedInOnlyView, ListView):
    model = models.ApartmentLease
    context_object_name = 'lists'
    template_name = 'books/apartmentlease/apartmentlease_list.html'


class ApartmentLeaseDetail(LoggedInOnlyView, DetailView):
    model = models.ApartmentLease
    # template_name = 'books/apartmentlease/apartmentlease_detail.html'
    template_name = 'books/detail_total.html'

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.realtor.pk != self.request.user.pk:
            raise Http404()
        return room


class ApartmentLeaseCreating(LoggedInOnlyView, CreateView):
    form_class = forms.ApartmentLeaseForm
    # template_name = 'books/apartmentlease/apartmentlease_creating.html'
    template_name = 'books/creating_total.html'

    def form_valid(self, form):
        book = form.save()
        book.realtor = self.request.user
        if book.bath is None:
            book.bath = 0
        if book.management_fee is None:
            book.management_fee = 0
        if book.total_area_m2 is None:
            book.total_area_m2 = 0
        if book.owner_phone is None:
            book.owner_phone = "-"
        if book.tenant_phone is None:
            book.tenant_phone = "-"
        book.save()
        return redirect(reverse("books:apartment-lease-detail", kwargs={"pk":book.pk}))
    # def get_success_url(self):
    #     return reverse("books:room-lease-list")   # 위 아래 둘 다 가능


class ApartmentLeaseUpdate(LoggedInOnlyView, UpdateView):
    model = models.ApartmentLease
    form_class = forms.ApartmentLeaseForm
    # template_name = "books/apartmentlease/apartmentlease_update.html"
    template_name = 'books/creating_total.html'
    

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.realtor.pk != self.request.user.pk:
            raise Http404()
        return room

    def form_valid(self, form):
        book = form.save()
        book.realtor = self.request.user
        if book.bath is None:
            book.bath = 0
        if book.management_fee is None:
            book.management_fee = 0
        if book.total_area_m2 is None:
            book.total_area_m2 = 0
        if book.owner_phone is None:
            book.owner_phone = "-"
        if book.tenant_phone is None:
            book.tenant_phone = "-"
        book.save()
        return redirect(reverse("books:apartment-lease-detail", kwargs={"pk":book.pk}))


def apartmentlease_search(request):

    address = request.GET.get("address")
    try:
        deposit = int(request.GET.get("deposit", 0))
    except:
        messages.error(request, "최대 보증금을 입력해주세요")
        return redirect(reverse("books:apartment-lease-list"))
    try:
        month_fee = int(request.GET.get("month_fee", 0))
    except:
        messages.error(request, "최대 월세를 입력해주세요")
        return redirect(reverse("books:apartment-lease-list"))
    try:
        area_m2 = int(request.GET.get("area_m2", 0))
    except:
        messages.error(request, "최소 면적을 입력해주세요")
        return redirect(reverse("books:apartment-lease-list"))
    room = request.GET.get("room", 0)
    parking = request.GET.get("parking")
    elevator = request.GET.get("elevator")
    loan = request.GET.get("loan")
    empty = request.GET.get("empty")
    not_finished = request.GET.get("not_finished")
    naver = request.GET.get("naver")
    dabang = request.GET.get("dabang")
    zicbang = request.GET.get("zicbang")
    peterpan = request.GET.get("peterpan")
    description = request.GET.get("description")
    
    filter_args = {}
    filter_args["address__contains"] = address
    filter_args["description__contains"] = description
    filter_args["deposit__lte"] = deposit
    filter_args["month_fee__lte"] = month_fee
    filter_args["area_m2__gte"] = area_m2
    filter_args["room__contains"] = room
    if parking == "on":
        filter_args["parking"] = True
    if elevator == "on":
        filter_args["elevator"] = True
    if loan == "on":
        filter_args["loan"] = True
    if empty == "on":
        filter_args["empty"] = True
    if not_finished == "on":
        filter_args["not_finished"] = True
    if naver == "on":
        filter_args["naver"] = True
    lists = models.ApartmentLease.objects.filter(**filter_args)
    return render(request, "books/apartmentlease/apartmentlease_search.html", {**filter_args, "lists": lists})


@login_required
def apartmentlease_delete(request, pk):
    room = models.ApartmentLease.objects.filter(pk=pk).delete()
    return redirect(reverse("books:apartment-lease-list"))

""""""
class OfficetelLeaseList(LoggedInOnlyView, ListView):
    model = models.OfficetelLease
    context_object_name = 'lists'
    template_name = 'books/officetellease/officetellease_list.html'


class OfficetelLeaseDetail(LoggedInOnlyView, DetailView):
    model = models.OfficetelLease
    # template_name = 'books/officetellease/officetellease_detail.html'
    template_name = 'books/detail_total.html'

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.realtor.pk != self.request.user.pk:
            raise Http404()
        return room


class OfficetelLeaseCreating(LoggedInOnlyView, CreateView):
    form_class = forms.OfficetelLeaseForm
    # template_name = 'books/officetellease/officetellease_creating.html'
    template_name = 'books/creating_total.html'

    def form_valid(self, form):
        book = form.save()
        book.realtor = self.request.user
        if book.bath is None:
            book.bath = 0
        if book.management_fee is None:
            book.management_fee = 0
        if book.total_area_m2 is None:
            book.total_area_m2 = 0
        if book.owner_phone is None:
            book.owner_phone = "-"
        if book.tenant_phone is None:
            book.tenant_phone = "-"
        book.save()
        return redirect(reverse("books:officetel-lease-detail", kwargs={"pk":book.pk}))


class OfficetelLeaseUpdate(LoggedInOnlyView, UpdateView):
    model = models.OfficetelLease
    form_class = forms.RoomLeaseForm
    # template_name = "books/officetellease/officetellease_update.html"
    template_name = 'books/creating_total.html'
    

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.realtor.pk != self.request.user.pk:
            raise Http404()
        return room

    def form_valid(self, form):
        book = form.save()
        book.realtor = self.request.user
        if book.bath is None:
            book.bath = 0
        if book.management_fee is None:
            book.management_fee = 0
        if book.total_area_m2 is None:
            book.total_area_m2 = 0
        if book.owner_phone is None:
            book.owner_phone = "-"
        if book.tenant_phone is None:
            book.tenant_phone = "-"
        book.save()
        return redirect(reverse("books:officetel-lease-detail", kwargs={"pk":book.pk}))


def officetellease_search(request):

    address = request.GET.get("address")
    try:
        deposit = int(request.GET.get("deposit", 0))
    except:
        messages.error(request, "최대 보증금을 입력해주세요")
        return redirect(reverse("books:officetel-lease-list"))
    try:
        month_fee = int(request.GET.get("month_fee", 0))
    except:
        messages.error(request, "최대 월세를 입력해주세요")
        return redirect(reverse("books:officetel-lease-list"))
    try:
        area_m2 = int(request.GET.get("area_m2", 0))
    except:
        messages.error(request, "최소 면적을 입력해주세요")
        return redirect(reverse("books:officetel-lease-list"))
    room = request.GET.get("room", 0)
    parking = request.GET.get("parking")
    elevator = request.GET.get("elevator")
    loan = request.GET.get("loan")
    empty = request.GET.get("empty")
    not_finished = request.GET.get("not_finished")
    naver = request.GET.get("naver")
    dabang = request.GET.get("dabang")
    zicbang = request.GET.get("zicbang")
    peterpan = request.GET.get("peterpan")
    description = request.GET.get("description")

    filter_args = {}
    filter_args["address__contains"] = address
    filter_args["description__contains"] = description
    filter_args["deposit__lte"] = deposit
    filter_args["month_fee__lte"] = month_fee
    filter_args["area_m2__gte"] = area_m2
    filter_args["room__contains"] = room
    if parking == "on":
        filter_args["parking"] = True
    if elevator == "on":
        filter_args["elevator"] = True
    if loan == "on":
        filter_args["loan"] = True
    if empty == "on":
        filter_args["empty"] = True
    if not_finished == "on":
        filter_args["not_finished"] = True
    if naver == "on":
        filter_args["naver"] = True
    if dabang == "on":
        filter_args["dabang"] = True
    if zicbang == "on":
        filter_args["zicbang"] = True
    if peterpan == "on":
        filter_args["peterpan"] = True
    lists = models.OfficetelLease.objects.filter(**filter_args)
    return render(request, "books/officetellease/officetellease_search.html", {**filter_args, "lists": lists})


@login_required
def officetellease_delete(request, pk):
    room = models.OfficetelLease.objects.filter(pk=pk).delete()
    return redirect(reverse("books:officetel-lease-list"))



class StoreLeaseList(LoggedInOnlyView, ListView):
    model = models.StoreLease
    context_object_name = 'lists'
    template_name = 'books/storelease/storelease_list.html'


class StoreLeaseDetail(LoggedInOnlyView, DetailView):
    model = models.StoreLease
    # template_name = 'books/storelease/storelease_detail.html'
    template_name = 'books/detail_total.html'

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.realtor.pk != self.request.user.pk:
            raise Http404()
        return room


class StoreLeaseCreating(LoggedInOnlyView, CreateView):
    form_class = forms.StoreLeaseForm
    # template_name = 'books/storelease/storelease_creating.html'
    template_name = 'books/creating_total.html'

    def form_valid(self, form):
        book = form.save()
        book.realtor = self.request.user
        if book.management_fee is None:
            book.management_fee = 0
        if book.total_area_m2 is None:
            book.total_area_m2 = 0
        if book.owner_phone is None:
            book.owner_phone = "-"
        if book.tenant_phone is None:
            book.tenant_phone = "-"
        if book.right_deposit is None:
            book.right_deposit = 0
        book.save()
        return redirect(reverse("books:store-lease-detail", kwargs={"pk":book.pk}))

    # def get_success_url(self):
    #     return reverse("books:room-lease-list")   # 위 아래 둘 다 가능


class StoreLeaseUpdate(LoggedInOnlyView, UpdateView):
    model = models.StoreLease
    form_class = forms.StoreLeaseForm
    # template_name = "books/storelease/storelease_update.html"
    template_name = 'books/creating_total.html'

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.realtor.pk != self.request.user.pk:
            raise Http404()
        return room

    def form_valid(self, form):
        book = form.save()
        book.realtor = self.request.user
        if book.management_fee is None:
            book.management_fee = 0
        if book.total_area_m2 is None:
            book.total_area_m2 = 0
        if book.owner_phone is None:
            book.owner_phone = "-"
        if book.tenant_phone is None:
            book.tenant_phone = "-"
        if book.right_deposit is None:
            book.right_deposit = 0
        book.save()
        return redirect(reverse("books:store-lease-detail", kwargs={"pk":book.pk}))


def storelease_search(request):

    address = request.GET.get("address")
    right_deposit = int(request.GET.get("right_deposit", 0))
    deposit = int(request.GET.get("deposit", 0))
    month_fee = int(request.GET.get("month_fee", 0))
    area_m2 = int(request.GET.get("area_m2", 0))
    parking = request.GET.get("parking")
    elevator = request.GET.get("elevator")
    empty = request.GET.get("empty")
    not_finished = request.GET.get("not_finished")
    naver = request.GET.get("naver")
    dabang = request.GET.get("dabang")
    zicbang = request.GET.get("zicbang")
    peterpan = request.GET.get("peterpan")
    description = request.GET.get("description")

    filter_args = {}
    filter_args["address__contains"] = address
    filter_args["description__contains"] = description
    filter_args["deposit__lte"] = deposit
    filter_args["month_fee__lte"] = month_fee
    filter_args["area_m2__gte"] = area_m2
    if parking == "on":
        filter_args["parking"] = True
    if elevator == "on":
        filter_args["elevator"] = True
    if empty == "on":
        filter_args["empty"] = True
    if not_finished == "on":
        filter_args["not_finished"] = True
    if naver == "on":
        filter_args["naver"] = True
    if  dabang == "on":
        filter_args["dabang"] = True
    if  zicbang == "on":
        filter_args["zicbang"] = True
    if  peterpan == "on":
        filter_args["peterpan"] = True
    lists = models.StoreLease.objects.filter(**filter_args)
    return render(request, "books/storelease/storelease_search.html", {**filter_args, "lists": lists})


@login_required
def storelease_delete(request, pk):
    room = models.StoreLease.objects.filter(pk=pk).delete()
    return redirect(reverse("books:store-lease-list"))

""""""

class RoomDealingList(LoggedInOnlyView, ListView):
    model = models.RoomDealing
    context_object_name = 'lists'
    template_name = 'books/roomdealing/roomdealing_list.html'


class RoomDealingDetail(LoggedInOnlyView, DetailView):
    model = models.RoomDealing
    # template_name = 'books/roomdealing/roomdealing_detail.html'
    template_name = 'books/detail_total.html'

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.realtor.pk != self.request.user.pk:
            raise Http404()
        return room


class RoomDealingCreating(LoggedInOnlyView, CreateView):
    form_class = forms.RoomDealingForm
    # template_name = 'books/roomdealing/roomdealing_creating.html'
    template_name = 'books/creating_total.html'

    def form_valid(self, form):
        book = form.save()
        book.realtor = self.request.user
        if book.bath is None:
            book.bath = 0
        if book.management_fee is None:
            book.management_fee = 0
        if book.total_area_m2 is None:
            book.total_area_m2 = 0
        if book.land_m2 is None:
            book.land_m2 = 0
        if book.owner_phone is None:
            book.owner_phone = "-"
        if book.tenant_phone is None:
            book.tenant_phone = "-"
        book.save()
        return redirect(reverse("books:room-dealing-detail", kwargs={"pk":book.pk}))


class RoomDealingUpdate(LoggedInOnlyView, UpdateView):
    model = models.RoomDealing
    form_class = forms.RoomDealingForm
    # template_name = "books/roomdealing/roomdealing_update.html"
    template_name = 'books/creating_total.html'

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.realtor.pk != self.request.user.pk:
            raise Http404()
        return room

    def form_valid(self, form):
        book = form.save()
        book.realtor = self.request.user
        if book.bath is None:
            book.bath = 0
        if book.management_fee is None:
            book.management_fee = 0
        if book.total_area_m2 is None:
            book.total_area_m2 = 0
        if book.land_m2 is None:
            book.land_m2 = 0
        if book.owner_phone is None:
            book.owner_phone = "-"
        if book.tenant_phone is None:
            book.tenant_phone = "-"
        book.save()
        return redirect(reverse("books:room-dealing-detail", kwargs={"pk":book.pk}))


def roomdealing_search(request):
    address = request.GET.get("address")
    price = int(request.GET.get("price", 0))
    area_m2 = int(request.GET.get("area_m2", 0))
    room = request.GET.get("room", 10)
    parking = request.GET.get("parking")
    elevator = request.GET.get("elevator")
    empty = request.GET.get("empty")
    not_finished = request.GET.get("not_finished")
    naver = request.GET.get("naver")
    dabang = request.GET.get("dabang")
    zicbang = request.GET.get("zicbang")
    peterpan = request.GET.get("peterpan")
    description = request.GET.get("description")
    
    filter_args = {}
    filter_args["address__contains"] = address
    filter_args["description__contains"] = description
    filter_args["price__lte"] = price
    filter_args["area_m2__gte"] = area_m2
    filter_args["room__gte"] = room
    if parking == "on":
        filter_args["parking"] = True
    if elevator == "on":
        filter_args["elevator"] = True
    if empty == "on":
        filter_args["empty"] = True
    if not_finished == "on":
        filter_args["not_finished"] = True
    if naver == "on":
        filter_args["naver"] = True
    if dabang == "on":
        filter_args["dabang"] = True
    if zicbang == "on":
        filter_args["zicbang"] = True
    if peterpan == "on":
        filter_args["peterpan"] = True
    lists = models.RoomDealing.objects.filter(**filter_args)
    return render(request, "books/roomdealing/roomdealing_search.html", {**filter_args, "lists": lists})


@login_required
def roomdealing_delete(request, pk):
    room = models.RoomDealing.objects.filter(pk=pk).delete()
    return redirect(reverse("books:room-dealing-list"))

""""""
class ApartmentDealingList(LoggedInOnlyView, ListView):
    model = models.ApartmentDealing
    context_object_name = 'lists'
    template_name = 'books/apartmentdealing/apartmentdealing_list.html'


class ApartmentDealingDetail(LoggedInOnlyView, DetailView):
    model = models.ApartmentDealing
    # template_name = 'books/apartmentdealing/apartmentdealing_detail.html'
    template_name = 'books/detail_total.html'

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.realtor.pk != self.request.user.pk:
            raise Http404()
        return room


class ApartmentDealingCreating(LoggedInOnlyView, CreateView):
    form_class = forms.ApartmentDealingForm
    # template_name = 'books/apartmentdealing/apartmentdealing_creating.html'
    template_name = 'books/creating_total.html'

    def form_valid(self, form):
        book = form.save()
        book.realtor = self.request.user
        if book.bath is None:
            book.bath = 0
        if book.management_fee is None:
            book.management_fee = 0
        if book.total_area_m2 is None:
            book.total_area_m2 = 0
        if book.land_m2 is None:
            book.land_m2 = 0
        if book.owner_phone is None:
            book.owner_phone = "-"
        if book.tenant_phone is None:
            book.tenant_phone = "-"
        book.save()
        return redirect(reverse("books:apartment-dealing-detail", kwargs={"pk":book.pk}))


class ApartmentDealingUpdate(LoggedInOnlyView, UpdateView):
    model = models.ApartmentDealing
    form_class = forms.ApartmentDealingForm
    # template_name = "books/apartmentdealing/apartmentdealing_update.html"
    template_name = 'books/creating_total.html'

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.realtor.pk != self.request.user.pk:
            raise Http404()
        return room

    def form_valid(self, form):
        book = form.save()
        book.realtor = self.request.user
        if book.bath is None:
            book.bath = 0
        if book.management_fee is None:
            book.management_fee = 0
        if book.total_area_m2 is None:
            book.total_area_m2 = 0
        if book.land_m2 is None:
            book.land_m2 = 0
        if book.owner_phone is None:
            book.owner_phone = "-"
        if book.tenant_phone is None:
            book.tenant_phone = "-"
        book.save()
        update = book
        
        return redirect(reverse("books:apartment-dealing-detail", kwargs={"pk":book.pk}))
        
def apartmentdealing_search(request):

    address = request.GET.get("address")
    price = int(request.GET.get("price", 0))
    area_m2 = int(request.GET.get("area_m2", 0))
    room = request.GET.get("room", 0)
    parking = request.GET.get("parking")
    elevator = request.GET.get("elevator")
    empty = request.GET.get("empty")
    not_finished = request.GET.get("not_finished")
    naver = request.GET.get("naver")
    dabang = request.GET.get("dabang")
    zicbang = request.GET.get("zicbang")
    peterpan = request.GET.get("peterpan")
    description = request.GET.get("description")
    
    filter_args = {}
    filter_args["address__contains"] = address
    filter_args["description__contains"] = description
    filter_args["price__lte"] = price
    filter_args["area_m2__gte"] = area_m2
    filter_args["room__contains"] = room
    if parking == "on":
        filter_args["parking"] = True
    if elevator == "on":
        filter_args["elevator"] = True
    if empty == "on":
        filter_args["empty"] = True
    if not_finished == "on":
        filter_args["not_finished"] = True
    if naver == "on":
        filter_args["naver"] = True
    if dabang == "on":
        filter_args["dabang"] = True
    if zicbang == "on":
        filter_args["zicbang"] = True
    if peterpan == "on":
        filter_args["peterpan"] = True
    lists = models.ApartmentDealing.objects.filter(**filter_args)
    return render(request, "books/apartmentdealing/apartmentdealing_search.html", {**filter_args, "lists": lists})


@login_required
def apartmentdealing_delete(request, pk):
    room = models.ApartmentDealing.objects.filter(pk=pk).delete()
    return redirect(reverse("books:apartment-dealing-list"))

""""""

class OfficetelDealingList(LoggedInOnlyView, ListView):
    model = models.OfficetelDealing
    context_object_name = 'lists'
    template_name = 'books/officeteldealing/officeteldealing_list.html'


class OfficetelDealingDetail(LoggedInOnlyView, DetailView):
    model = models.OfficetelDealing
    # template_name = 'books/officeteldealing/officeteldealing_detail.html'
    template_name = 'books/detail_total.html'

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.realtor.pk != self.request.user.pk:
            raise Http404()
        return room


class OfficetelDealingCreating(LoggedInOnlyView, CreateView):
    form_class = forms.OfficetelDealingForm
    # template_name = 'books/officeteldealing/officeteldealing_creating.html'
    template_name = 'books/creating_total.html'

    def form_valid(self, form):
        book = form.save()
        book.realtor = self.request.user
        if book.bath is None:
            book.bath = 0
        if book.management_fee is None:
            book.management_fee = 0
        if book.total_area_m2 is None:
            book.total_area_m2 = 0
        if book.land_m2 is None:
            book.land_m2 = 0
        if book.owner_phone is None:
            book.owner_phone = "-"
        if book.tenant_phone is None:
            book.tenant_phone = "-"
        book.save()
        return redirect(reverse("books:officetel-dealing-detail", kwargs={"pk":book.pk}))


class OfficetelDealingUpdate(LoggedInOnlyView, UpdateView):
    model = models.OfficetelDealing
    form_class = forms.OfficetelDealingForm
    # template_name = "books/officeteldealing/officeteldealing_update.html"
    template_name = 'books/creating_total.html'

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.realtor.pk != self.request.user.pk:
            raise Http404()
        return room

    def form_valid(self, form):
        book = form.save()
        book.realtor = self.request.user
        if book.bath is None:
            book.bath = 0
        if book.management_fee is None:
            book.management_fee = 0
        if book.total_area_m2 is None:
            book.total_area_m2 = 0
        if book.land_m2 is None:
            book.land_m2 = 0
        if book.owner_phone is None:
            book.owner_phone = "-"
        if book.tenant_phone is None:
            book.tenant_phone = "-"
        book.save()
        return redirect(reverse("books:officetel-dealing-detail", kwargs={"pk":book.pk}))


def officeteldealing_search(request):

    address = request.GET.get("address")
    price = int(request.GET.get("price", 0))
    area_m2 = int(request.GET.get("area_m2", 0))
    room = request.GET.get("room", 0)
    parking = request.GET.get("parking")
    elevator = request.GET.get("elevator")
    empty = request.GET.get("empty")
    not_finished = request.GET.get("not_finished")
    naver = request.GET.get("naver")
    dabang = request.GET.get("dabang")
    zicbang = request.GET.get("zicbang")
    peterpan = request.GET.get("peterpan")
    description = request.GET.get("description")
    
    filter_args = {}
    filter_args["address__contains"] = address
    filter_args["description__contains"] = description
    filter_args["price__lte"] = price
    filter_args["area_m2__gte"] = area_m2
    filter_args["room__contains"] = room
    if parking == "on":
        filter_args["parking"] = True
    if elevator == "on":
        filter_args["elevator"] = True
    if empty == "on":
        filter_args["empty"] = True
    if not_finished == "on":
        filter_args["not_finished"] = True
    if naver == "on":
        filter_args["naver"] = True
    if dabang == "on":
        filter_args["dabang"] = True
    if zicbang == "on":
        filter_args["zicbang"] = True
    if peterpan == "on":
        filter_args["peterpan"] = True
    lists = models.OfficetelDealing.objects.filter(**filter_args)
    return render(request, "books/officeteldealing/officeteldealing_search.html", {**filter_args, "lists": lists})


@login_required
def officeteldealing_delete(request, pk):
    room = models.OfficetelDealing.objects.filter(pk=pk).delete()
    return redirect(reverse("books:officetel-dealing-list"))

""""""

class StoreDealingList(LoggedInOnlyView, ListView):
    model = models.StoreDealing
    context_object_name = 'lists'
    template_name = 'books/storedealing/storedealing_list.html'


class StoreDealingDetail(LoggedInOnlyView, DetailView):
    model = models.StoreDealing
    # template_name = 'books/storedealing/storedealing_detail.html'
    template_name = 'books/detail_total.html'

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.realtor.pk != self.request.user.pk:
            raise Http404()
        return room


class StoreDealingCreating(LoggedInOnlyView, CreateView):
    form_class = forms.StoreDealingForm
    # template_name = 'books/storedealing/storedealing_creating.html'
    template_name = 'books/creating_total.html'

    def form_valid(self, form):
        book = form.save()
        book.realtor = self.request.user
        if book.management_fee is None:
            book.management_fee = 0
        if book.total_area_m2 is None:
            book.total_area_m2 = 0
        if book.land_m2 is None:
            book.land_m2 = 0
        if book.owner_phone is None:
            book.owner_phone = "-"
        if book.tenant_phone is None:
            book.tenant_phone = "-"
        book.save()
        return redirect(reverse("books:store-dealing-detail", kwargs={"pk":book.pk}))


class StoreDealingUpdate(LoggedInOnlyView, UpdateView):
    model = models.StoreDealing
    form_class = forms.StoreDealingForm
    # template_name = "books/storedealing/storedealing_update.html"
    template_name = 'books/creating_total.html'

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.realtor.pk != self.request.user.pk:
            raise Http404()
        return room

    def form_valid(self, form):
        book = form.save()
        book.realtor = self.request.user
        if book.management_fee is None:
            book.management_fee = 0
        if book.total_area_m2 is None:
            book.total_area_m2 = 0
        if book.land_m2 is None:
            book.land_m2 = 0
        if book.owner_phone is None:
            book.owner_phone = "-"
        if book.tenant_phone is None:
            book.tenant_phone = "-"
        book.save()
        return redirect(reverse("books:store-dealing-detail", kwargs={"pk":book.pk}))


def storedealing_search(request):

    address = request.GET.get("address")
    price = int(request.GET.get("price", 0))
    area_m2 = int(request.GET.get("area_m2", 0))
    parking = request.GET.get("parking")
    elevator = request.GET.get("elevator")
    empty = request.GET.get("empty")
    not_finished = request.GET.get("not_finished")
    naver = request.GET.get("naver")
    dabang = request.GET.get("dabang")
    zicbang = request.GET.get("zicbang")
    peterpan = request.GET.get("peterpan")
    description = request.GET.get("description")
    
    filter_args = {}
    filter_args["address__contains"] = address
    filter_args["description__contains"] = description
    filter_args["price__lte"] = price
    filter_args["area_m2__gte"] = area_m2
    if parking == "on":
        filter_args["parking"] = True
    if elevator == "on":
        filter_args["elevator"] = True
    if empty == "on":
        filter_args["empty"] = True
    if not_finished == "on":
        filter_args["not_finished"] = True
    if naver == "on":
        filter_args["naver"] = True
    if dabang == "on":
        filter_args["dabang"] = True
    if zicbang == "on":
        filter_args["zicbang"] = True
    if peterpan == "on":
        filter_args["peterpan"] = True
    lists = models.StoreDealing.objects.filter(**filter_args)
    return render(request, "books/storedealing/storedealing_search.html", {**filter_args, "lists": lists})


@login_required
def storedealing_delete(request, pk):
    room = models.StoreDealing.objects.filter(pk=pk).delete()
    return redirect(reverse("books:store-dealing-list"))

""""""
class BuildingDealingList(LoggedInOnlyView, ListView):
    model = models.BuildingDealing
    context_object_name = 'buildingdealing'
    template_name = 'books/buildingdealing/buildingdealing_list.html'


class BuildingDealingDetail(LoggedInOnlyView, DetailView):
    model = models.BuildingDealing
    # template_name = 'books/buildingdealing/buildingdealing_detail.html'
    template_name = 'books/detail_total.html'

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.realtor.pk != self.request.user.pk:
            raise Http404()
        return room


class BuildingDealingCreating(LoggedInOnlyView, CreateView):
    form_class = forms.BuildingDealingForm
    # template_name = 'books/buildingdealing/buildingdealing_creating.html'
    template_name = 'books/creating_total.html'

    def form_valid(self, form):
        book = form.save()
        book.realtor = self.request.user
        if book.land_m2 is None:
            book.land_m2 = 0
        if book.land_type is None:
            book.land_type = "-"
        if book.management_fee is None:
            book.management_fee = 0
        if book.floor_top is None:
            book.floor_top = 0
        if book.floor_bottom is None:
            book.floor_bottom = 0
        if book.total_floor_area_m2 is None:
            book.total_floor_area_m2 = 0
        if book.total_floor_area_m2_for_ratio is None:
            book.total_floor_area_m2_for_ratio = 0
        if book.building_area_m2 is None:
            book.building_area_m2 = 0
        if book.floor_area_ratio is None:
            book.floor_area_ratio = 0
        if book.building_coverage is None:
            book.building_coverage = 0
        if book.parking_number is None:
            book.parking_number = 0
        if book.owner_phone is None:
            book.owner_phone = "-"
        if book.tenant_phone is None:
            book.tenant_phone = "-"
        book.save()
        return redirect(reverse("books:building-dealing-detail", kwargs={"pk":book.pk}))


class BuildingDealingUpdate(LoggedInOnlyView, UpdateView):
    model = models.BuildingDealing
    form_class = forms.BuildingDealingForm
    # template_name = "books/buildingdealing/buildingdealing_update.html"
    template_name = 'books/creating_total.html'

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
        if book.land_type is None:
            book.land_type = "-"
        if book.management_fee is None:
            book.management_fee = 0
        if book.floor_top is None:
            book.floor_top = 0
        if book.floor_bottom is None:
            book.floor_bottom = 0
        if book.total_floor_area_m2 is None:
            book.total_floor_area_m2 = 0
        if book.total_floor_area_m2_for_ratio is None:
            book.total_floor_area_m2_for_ratio = 0
        if book.building_area_m2 is None:
            book.building_area_m2 = 0
        if book.floor_area_ratio is None:
            book.floor_area_ratio = 0
        if book.building_coverage is None:
            book.building_coverage = 0
        if book.parking_number is None:
            book.parking_number = 0
        if book.owner_phone is None:
            book.owner_phone = "-"
        if book.tenant_phone is None:
            book.tenant_phone = "-"
        book.save()
        return redirect(reverse("books:building-dealing-detail", kwargs={"pk":book.pk}))


def buildingdealing_search(request):

    address = request.GET.get("address")
    price = int(request.GET.get("price", 0))
    land_m2 = int(request.GET.get("area_m2", 0))
    elevator = request.GET.get("elevator")
    not_finished = request.GET.get("not_finished")
    naver = request.GET.get("naver")
    dabang = request.GET.get("dabang")
    zicbang = request.GET.get("zicbang")
    peterpan = request.GET.get("peterpan")
    description = request.GET.get("description")

    filter_args = {}
    filter_args["address__contains"] = address
    filter_args["description__contains"] = description
    filter_args["price__lte"] = price
    filter_args["land_m2__gte"] = land_m2
    if elevator == "on":
        filter_args["elevator"] = True
    if not_finished == "on":
        filter_args["not_finished"] = True
    if naver == "on":
        filter_args["naver"] = True
    if dabang == "on":
        filter_args["dabang"] = True
    if zicbang == "on":
        filter_args["zicbang"] = True
    if peterpan == "on":
        filter_args["peterpan"] = True
    lists = models.BuildingDealing.objects.filter(**filter_args)
    return render(request, "books/buildingdealing/buildingdealing_search.html", {**filter_args, "lists": lists})


@login_required
def buildingdealing_delete(request, pk):
    building = models.BuildingDealing.objects.filter(pk=pk).delete()
    return redirect(reverse("books:building-dealing-list"))
