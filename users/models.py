import uuid
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string


class User(AbstractUser):
    """ Custom User Model"""
    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"
    LOGIN_KAKAO = "kakao"
    LOGIN_NAVER = "naver"
    LOGIN_CHOICES = ((LOGIN_EMAIL, "Email"),(LOGIN_GITHUB, "Github"), (LOGIN_KAKAO, "Kakao"), (LOGIN_NAVER, "Naver"))

    user_id = models.BigAutoField(primary_key=True)
    login_method = models.CharField(
        max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars", blank=True)
    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=20, default="", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    objects = UserManager() # eb deploy를 할때 command로 createsuperuser를 하기 위해 작성 -> users/management/commands/createsu.py를 보자

    def verify_email(self):
        if self.email_verified is False:
            secret=uuid.uuid4().hex[:20]
            self.email_secret = secret
            if settings.DEBUG == True:
                html_message = render_to_string(
                "emails/verify_email_dev.html", {"secret":secret} 
                )
            else:
                html_message = render_to_string(
                "emails/verify_email_deploy.html", {"secret":secret} 
                )
            send_mail(
                "탈탈부동산 회원가입 인증 메일입니다.", 
                strip_tags(html_message), 
                settings.EMAIL_HOST_USER,
                [self.email],
                fail_silently = False,
                html_message=html_message,
            )
            self.save()
        else:
            messages.error(self.request, "E!!!!!")

    def get_absolute_url(self):
        return reverse("users:status", kwargs={"pk": self.pk})
