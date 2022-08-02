import yagmail, time
from datetime import timedelta, date
from django.conf import settings
from django.http import Http404
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from . import models, forms
from users import models as users_model
from components.search_filter import search_filter


class LoggedInOnlyView(LoginRequiredMixin):
    login_url = reverse_lazy('users:login')
    

class ManagementList(LoggedInOnlyView, ListView):
    model = models.Management
    context_object_name = "lists"

def management_search(request):
    filter_args = search_filter(request)
    lists = models.Management.objects.filter(**filter_args)
    return render(request, "managements/management_list.html", {**filter_args, "lists": lists})


class ManagementCreating(LoggedInOnlyView, CreateView):
    form_class = forms.ManagementForm
    template_name = 'managements/management_creating.html'

    def form_valid(self, form):
        management = form.save()
        management.realtor = self.request.user
        management.save()
        return redirect(reverse("managements:detail", kwargs={"pk":management.pk}))


class ManagementUpdate(LoggedInOnlyView, UpdateView):
    model = models.Management
    form_class = forms.ManagementForm
    template_name = 'managements/management_creating.html'

    def get_object(self, queryset=None):
        management = super().get_object(queryset=queryset)
        if management.realtor.pk != self.request.user.pk:
            raise Http404()
        return management

    def form_valid(self, form):
        management = form.save()
        management.realtor = self.request.user
        management.save()
        return redirect(reverse("managements:detail", kwargs={"pk":management.pk}))



class ManagementDetail(LoggedInOnlyView, DetailView):
    model = models.Management
    template_name = 'managements/management_detail.html'

    def get_object(self, queryset=None):
        management = super().get_object(queryset=queryset)
        return management
    

@login_required
def management_delete(request, pk):
    management = models.Management.objects.filter(pk=pk)
    management.delete()
    return redirect(reverse("managements:list"))


class ManagementMailing(LoggedInOnlyView, View):
    def get(self, request):
        if request.user.is_staff:
            users = users_model.User.objects.all()
            for user in users:
                lease_renewal_dict = {}
                lease_report_dict = {}
                for management in user.managements.all():
                    if (60 <= (management.contract_last_day - date.today()).days <= 180) and management.deal_renewal_notice is False:
                        lease_renewal_dict.update({management.address: (management.contract_last_day - date.today()).days})
                    if (management.contract_day - date.today()).days + 30 <=7 and management.deal_report is False:
                        lease_report_dict.update({management.address: (management.contract_day - date.today()).days + 30})
                if len(lease_renewal_dict) > 0:
                    renewal_html_message = render_to_string(
                                "emails/lease_renewal_email.html", {"lease_renewal_dict": lease_renewal_dict}
                            )
                            
                    send_mail(
                            "계약 갱신 고지 매물 : {}".format(date.today()),
                            strip_tags(""),
                            settings.EMAIL_HOST_USER,
                            [user.email],
                            fail_silently = False,
                            html_message= renewal_html_message
                        )
                if len(lease_report_dict) > 0:
                    report_html_message = render_to_string(
                                "emails/lease_report_email.html", {"lease_report_dict": lease_report_dict}
                            )
                            
                    send_mail(
                            "전월세 거래신고 매물 : {}".format(date.today()),
                            strip_tags(""),
                            settings.EMAIL_HOST_USER,
                            [user.email],
                            fail_silently = False,
                            html_message= report_html_message
                        )
            time.sleep(5)    
            return render(request, 'managements/mailing.html')
        else:
            raise Http404()