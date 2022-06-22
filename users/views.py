import os
import requests
import uuid
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import FormView, View, ListView, UpdateView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
# from verify_email.email_handler import send_verification_email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.html import strip_tags
# from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from validate_email import validate_email       # pipenv install validate_email
from . import forms, models



class LoggedOutOnlyView(UserPassesTestMixin, View):
    def test_func(self):
        return not self.request.user.is_authenticated

class LoggedInOnlyView(LoginRequiredMixin):
    login_url = reverse_lazy('users:login')


class SignUpView(LoggedOutOnlyView, FormView):
    template_name = 'users/signup.html'
    form_class = forms.SignUpForm
    success_url = reverse_lazy('users:signup-after')

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')         
        user = authenticate(self.request, username=email, password=password)
        user.verify_email()
        return super().form_valid(form)

class SignUpAfterView(LoggedOutOnlyView, FormView):
    template_name = 'users/signup_after.html'
    form_class = forms.SignUpForm


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
    except models.User.DoesNotExist:
        pass
    return redirect(reverse("users:login"))


class LoginException(Exception):
    pass 


class LoginView(LoggedOutOnlyView, FormView):
    template_name = 'users/login.html'
    form_class = forms.LoginForm
    success_url = reverse_lazy('core:home')

    def form_valid(self, form):  
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=email, password=password)
        user_model = models.User.objects.get(email=email)
        # if user_model.email_verified:
        login(self.request, user)                   
        # else:
        #     messages.info(self.request, "이메일을 확인하여 인증을 완료해주세요.")
        #     user.verify_email()
        return super().form_valid(form) 
        
        
def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))

class UserStatusView(LoggedInOnlyView, ListView):
    model = models.User
    template_name = "users/status.html"

    def get_object(self, queryset=None):
        user = super().get_object(queryset=queryset)
        if user.realtor.pk != self.request.user.pk:
            raise Http404()
        return user


"""UpdatePasswordView 1"""
# class UpdatePasswordView(LoggedInOnlyView, PasswordChangeView):
#     form_class = PasswordChangeForm
#     template_name = "users/update-password.html"

#     def get_form(self, form_class=None):
    
#         form = super().get_form(form_class=form_class)
#         form.fields["old_password"].widget.attrs = {"placeholder": "Old Password"}
#         form.fields["new_password1"].widget.attrs = {"placeholder": "New Password"}
#         form.fields["new_password2"].widget.attrs = {"placeholder": "New Password Confirm"}
#         return form        


#     def get_success_url(self):
#         return self.request.user.get_absolute_url()

"""UpdatePasswordView 2"""
class UpdatePasswordView(LoggedInOnlyView, PasswordChangeView):
    form_class = forms.UpdatePasswordForm
    template_name = "users/update-password.html"

    def get_success_url(self):
        return self.request.user.get_absolute_url()

"""회원탈퇴: https://parkhyeonchae.github.io/2020/03/31/django-project-15/"""
@login_required
def user_del(request):
    if request.method == 'POST':
        password_form = forms.CheckPasswordForm(request.user, request.POST)
        
        if password_form.is_valid():
            request.user.delete()
            logout(request)
            messages.success(request, "회원탈퇴가 완료되었습니다.")
            return redirect('core:home')
    else:
        password_form = forms.CheckPasswordForm(request.user)

    return render(request, 'users/user_del.html', {'password_form':password_form})




class RequestPasswordResetEmail(LoggedOutOnlyView, View):
    def get(self, request):
        return render(request, 'users/reset-password.html')

    def post(self, request):
        email = request.POST['email']
        context = {'values':request.POST}
        if not validate_email(email):
            messages.error(request, "올바른 이메일을 입력해주세요")
            return render(request, 'users/reset-password.html', context)        
        
        current_site = get_current_site(request)
        user = models.User.objects.filter(email=email)
        
        if user.exists():
            if user[0].login_method == 'email':
                email_contents = {
                    'user':user[0],
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                    'token': PasswordResetTokenGenerator().make_token(user[0]),
                }
                link = reverse('users:reset-user-password', kwargs={'uidb64':email_contents['uid'], 'token':email_contents['token']})
                email_subject = '탈탈부동산 비밀번호 재설정 이메일입니다'
                reset_url = 'http://' + current_site.domain + link
                
                # html_message = render_to_string(
                #     "emails/password_reset_email.html", {"reset_url":reset_url}
                # )
                # email_message = EmailMessage(
                #     email_subject,
                #     strip_tags(html_message),
                #     settings.EMAIL_HOST_USER,
                #     [email],
                # )
                # email_message.send(fail_silently=False)
            
                html_message = render_to_string(
                    "emails/password_reset_email.html", {"reset_url":reset_url}
                )
                send_mail(
                    email_subject,
                    strip_tags(html_message),
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently = False,
                    html_message = html_message,
                )
                
            else:
                messages.error(request, "비밀번호를 바꿀 수 없는 아이디입니다.")
                return render(request, 'users/reset-password.html', context)   
        else:
            messages.error(request, "가입되지 않은 이메일입니다.")
            return redirect("users:request-password")
        return render(request, 'users/sending-password-email-done.html')
    

class CompletePasswordReset(LoggedOutOnlyView, View):
    
    def get(self, request, uidb64, token):    
        context = {'uidb64':uidb64, 'token': token}
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = models.User.objects.get(pk=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(request, '새로운 인증메일 링크를 이용해주세요')
                return render(request, 'users/reset-password.html')
        except:
            pass
        return render(request, 'users/set-new-password.html', context)
  
    def post(self, request, uidb64, token):
        context = {'uidb64':uidb64, 'token': token}
        password = request.POST['password']
        password1 = request.POST['password1']
        if password != password1:
            messages.error(request, '비밀번호가 일치하지 않습니다')
            return render(request, 'users/set-new-password.html', context)
        if len(password) < 6:
            messages.error(request, '6 글자 이상으로 설정해주세요')
            return render(request, 'users/set-new-password.html', context)
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = models.User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request, '비밀번호가 정상적으로 바뀌었습니다')
            return redirect('users:login')
        except:
            messages.info(request, 'Somethin went wrong')
            return render(request, 'users/set-new-password.html', context)
            
class SendingPasswordEmailDone(LoggedOutOnlyView, View):        
    template_name = "users/sending-email-done.html"


def github_login(request):
    if settings.DEBUG == True:
        client_id = os.environ.get("GH_ID")
        redirect_uri = "http://127.0.0.1:8000/users/login/github/callback/"
    else:
        client_id = os.environ.get("GH_ID_DEPLOY")
        redirect_uri = "http://taltalrealty31-dev.ap-northeast-2.elasticbeanstalk.com/users/login/github/callback/"
    return redirect(f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user")


def github_callback(request):
    if settings.DEBUG == True:
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
    else:
        client_id = os.environ.get("GH_ID_DEPLOY")
        client_secret = os.environ.get("GH_SECRET_DEPLOY")
    code = request.GET.get("code")
    result = requests.post(
        f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
        headers={"Accept": "application/json"},)
    result_json = result.json()
    access_token = result_json.get("access_token")
    profile_request = requests.get(
        "https://api.github.com/user",
        headers={
            "Authorization": f"token {access_token}",
            "Accept": "application/json"})
    profile_json = profile_request.json()
    print(profile_json)
    email = profile_json.get("email")
    bio = profile_json.get("bio")
    bio = "" if bio is None else bio
    try:
        user = models.User.objects.get(email=email)
        if user.login_method != models.User.LOGIN_GITHUB:
            messages.error(request, "다른 경로로 가입되어있는 이메일입니다")
            return redirect("users:login")
    except models.User.DoesNotExist:
        user = models.User.objects.create(
            username=email, email=email,
            bio=bio, login_method=models.User.LOGIN_GITHUB)
        user.set_unusable_password()
        user.email_verified = True
        user.save()
    login(request, user)
    return redirect(reverse("core:home"))


def kakao_login(request):
    if settings.DEBUG == True:
        REST_API_KEY = os.environ.get("KAKAO_ID")
        REDIRECT_URI = "http://127.0.0.1:8000/users/login/kakao/callback/"
    else:
        REST_API_KEY = os.environ.get("KAKAO_ID_DEPLOY")
        REDIRECT_URI = "http://taltalrealty31-dev.ap-northeast-2.elasticbeanstalk.com/users/login/kakao/callback/"
    return redirect(f"https://kauth.kakao.com/oauth/authorize?client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&response_type=code")


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        if settings.DEBUG == True:
            REST_API_KEY = os.environ.get("KAKAO_ID")
            REDIRECT_URI = "http://127.0.0.1:8000/users/login/kakao/callback/"
        else:
            REST_API_KEY = os.environ.get("KAKAO_ID_DEPLOY")
            REDIRECT_URI = "http://taltalrealty31-dev.ap-northeast-2.elasticbeanstalk.com/users/login/kakao/callback/"
        code = request.GET.get("code")
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&code={code}")
        token_json = token_request.json()
        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={
                "Authorization": f"Bearer {access_token}", })
        profile_json = profile_request.json()
        properties = profile_json.get("properties")
        kakao_account = profile_json.get("kakao_account")
        email = kakao_account.get("email")
        nickname = properties.get("nickname")
        profile_image = properties.get("profile_image")
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_KAKAO:
                messages.error(request, "다른 경로로 가입되어있는 이메일입니다")
                return redirect("users:login")
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                login_method=models.User.LOGIN_KAKAO,
            )
            user.set_unusable_password()
            user.email_verified = True
            user.save()
            if profile_image is not None:
                photo_request = requests.get(profile_image)
                user.avatar.save(f"{nickname}-avatar",
                                ContentFile(photo_request.content))
        login(request, user)
        return redirect(reverse("core:home"))
    except KakaoException:
        return redirect(reverse("users:login"))


def kakao_login_app(request):
    if settings.DEBUG == True:
        REST_API_KEY = os.environ.get("KAKAO_ID")
        REDIRECT_URI = "https://cb3b-112-187-140-235.jp.ngrok.io/api/v1/users/social-login/"
    else:
        REST_API_KEY = os.environ.get("KAKAO_ID_DEPLOY")
        REDIRECT_URI = "http://taltalrealty31-dev.ap-northeast-2.elasticbeanstalk.com/api/v1/users/social-login/"
    return redirect(f"https://kauth.kakao.com/oauth/authorize?client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&response_type=code")


def kakao_callback_app(request):
    try:
        if settings.DEBUG == True:
            REST_API_KEY = os.environ.get("KAKAO_ID")
            REDIRECT_URI = "https://24a5-175-193-30-213.jp.ngrok.io/users/login/kakao-app/callback/"
        else:
            REST_API_KEY = os.environ.get("KAKAO_ID_DEPLOY")
            REDIRECT_URI = "http://taltalrealty31-dev.ap-northeast-2.elasticbeanstalk.com/users/login/kakao-app/callback/"
        code = request.GET.get("code")
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&code={code}")
        token_json = token_request.json()
        access_token = token_json.get("access_token")
        print(access_token)
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={
                "Authorization": f"Bearer {access_token}", })
        profile_json = profile_request.json()
        properties = profile_json.get("properties")
        kakao_account = profile_json.get("kakao_account")
        email = kakao_account.get("email")
        nickname = properties.get("nickname")
        profile_image = properties.get("profile_image")
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_KAKAO:
                messages.error(request, "다른 경로로 가입되어있는 이메일입니다")
                return redirect("users:login")
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                login_method=models.User.LOGIN_KAKAO,
            )
            user.set_unusable_password()
            user.email_verified = True
            user.save()
            if profile_image is not None:
                photo_request = requests.get(profile_image)
                user.avatar.save(f"{nickname}-avatar",
                                ContentFile(photo_request.content))
        login(request, user)
        get_user = models.User.objects.get(username=user.username)
        print(get_user.username)
        print(get_user.pk)
        # return redirect(reverse("core:home"))
        return render(request, 'app_token.html', {"access_token":access_token, "email":email, "user_pk":get_user.pk})
    except KakaoException:
        return redirect(reverse("users:login"))

def naver_login(request):
    if settings.DEBUG == True:
        client_id = os.environ.get("NAVER_ID")
        redirect_uri = "http://127.0.0.1:8000/users/login/naver/callback/"
    else:
        client_id = os.environ.get("NAVER_ID_DEPLOY")
        redirect_uri = "http://taltalrealty31-dev.ap-northeast-2.elasticbeanstalk.com/users/login/naver/callback/"
    state = uuid.uuid4().hex[:20]
    return redirect(f"https://nid.naver.com/oauth2.0/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&state={state}")



def naver_callback(request):
    if settings.DEBUG == True:
        client_id = os.environ.get("NAVER_ID")
        client_secret = os.environ.get("NAVER_SECRET")
    else:
        client_id = os.environ.get("NAVER_ID_DEPLOY")
        client_secret = os.environ.get("NAVER_SECRET_DEPLOY")
    code = request.GET.get("code")
    state = request.GET.get("state")
    token_request = requests.post(
        f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&code={code}&state={state}"
    )
    token_json = token_request.json()
    access_token = token_json.get("access_token")
    profile_request = requests.get(
        "https://openapi.naver.com/v1/nid/me",
        headers={
            "Authorization": f"Bearer {access_token}",
        }
    )
    profile_json = profile_request.json()
    response = profile_json.get("response")
    print(response)
    email = response.get("email")
    try:
        user = models.User.objects.get(email=email)
        if user.login_method != models.User.LOGIN_NAVER:
            messages.error(request, "다른 경로로 가입되어있는 이메일입니다")
            return redirect("users:login")
    except models.User.DoesNotExist:
        user = models.User.objects.create(
            email=email,
            username=email,
            login_method=models.User.LOGIN_NAVER
        )
        user.set_unusable_password()
        user.email_verified = True
        user.save()
    login(request,user)
    return redirect(reverse("core:home"))


class WebViewSample(View):
    def get(self, request):
        return render(request, 'users/webview_sample.html')