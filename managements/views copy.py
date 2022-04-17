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


class LoggedInOnlyView(LoginRequiredMixin):
    login_url = reverse_lazy('users:login')
    

class ManagementList(LoggedInOnlyView, ListView):
    model = models.Management
    context_object_name = "lists"


class ManagementCreating(LoggedInOnlyView, CreateView):
    form_class = forms.ManagementForm
    template_name = 'managements/management_creating.html'

    def form_valid(self, form):
        management = form.save()
        management.manager = self.request.user
        management.save()
        return redirect(reverse("managements:detail", kwargs={"pk":management.pk}))


class ManagementUpdate(LoggedInOnlyView, UpdateView):
    model = models.Management
    form_class = forms.ManagementForm
    template_name = 'managements/management_creating.html'

    def get_object(self, queryset=None):
        management = super().get_object(queryset=queryset)
        if management.manager.pk != self.request.user.pk:
            raise Http404()
        return management

    def form_valid(self, form):
        management = form.save()
        management.manager = self.request.user
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
    management = models.Management.objects.filter(pk=pk).delete()
    return redirect(reverse("managements:list"))


class ManagementMailing(LoggedInOnlyView, View):
    def get(self, request):
        if request.user.is_staff:
            while True:        
                users = users_model.User.objects.all()
                for user in users:
                    address_dict = {}
                    for management in user.managements.all():
                        
                        # if 180 < (management.contract_last_day - date.today()).days:
                        #     print(management.address, "180~")
                        # if 150 < (management.contract_last_day - date.today()).days <= 180:
                        #     print(management.address, "150~")
                        # if 120 < (management.contract_last_day - date.today()).days <= 150:
                        #     print(management.address,"120~")
                        # if 90 < (management.contract_last_day - date.today()).days <= 120:
                        #     print(management.address,"90~")
                        # if 60 < (management.contract_last_day - date.today()).days <= 90:
                        #     print(management.address,"60~")
                        # if 30 < (management.contract_last_day - date.today()).days <= 60:
                        #     print(management.address,"30~")
                        # if 0 < (management.contract_last_day - date.today()).days <= 30:
                        #     print(management.address,"0~")
                            
                        if (60 <= (management.contract_last_day - date.today()).days <= 180) and management.deal_renewal_notice is False:
                            
                            address_dict.update({management.address: (management.contract_last_day - date.today()).days})
                            print(address_dict)
                            
                        # elif (management.contract_last_day - date.today()).days > 180:
                        #     address_dict.update({management.address: (management.contract_last_day - date.today()).days})
                        #     print(address_dict)
                        # else:
                        #     address_dict.update({management.address: (management.contract_last_day - date.today()).days})
                        #     print(address_dict)
                            
                        # print(management.address)
                        # address_list.append(management.address)
                    #     print(address_list)
                    
                    html_message = render_to_string(
                                "emails/management_email.html", {"address_dict": address_dict}
                            )
                            
                    send_mail(
                            "메일테스트",
                            strip_tags(""),
                            settings.EMAIL_HOST_USER,
                            [user.email],
                            fail_silently = False,
                            html_message= html_message
                        )
                time.sleep(5)    
            return render(request, 'managements/mailing.html')
        else:
            raise Http404()