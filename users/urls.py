from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name='signup'),
    path("signup/after/", views.SignUpAfterView.as_view(), name="signup-after"),
    # path("activate/<uidb64>/<token>/", views.VerificationView.as_view(), name='activate'),
    path("verify/<str:key>", views.complete_verification, name="complete-verification"),
    path("login/", views.LoginView.as_view(), name='login'),
    path("login/github/", views.github_login, name="github-login"),
    path("login/github/callback/", views.github_callback, name="github-callback"),
    path("login/kakao/", views.kakao_login, name="kakao-login"),
    path("login/kakao/callback/", views.kakao_callback, name="kakao-callback"),

    path("login/app/", views.AppLoginView.as_view(), name="login-app"),

    path("login/kakao-app/", views.kakao_login_app, name="kakao-login-app"),
    path("login/kakao-app/callback/", views.kakao_callback_app, name="kakao-callback-app"),
    
    path("login/naver/", views.naver_login, name="naver-login"),
    path("login/naver/callback/", views.naver_callback, name="naver-callback"),
    path("logout/", views.log_out, name="logout"),
    path("status/<int:pk>/", views.UserStatusView.as_view(), name="status"),
    path("changepassword/<int:pk>/", views.UpdatePasswordView.as_view(), name="change-password"),
    path("user_del/", views.user_del, name="user_del"),
    # path("update-password/", views.UpdatePasswordView.as_view(), name="update-password"),
    path("request-reset-link/", views.RequestPasswordResetEmail.as_view(), name="request-password"),
    path("set-new-password/<uidb64>/<token>/", views.CompletePasswordReset.as_view(), name="reset-user-password"),
    path("sending-password-email-done/", views.SendingPasswordEmailDone.as_view(), name="sending-passowrd-email-done"),
    path("webview-sample/", views.WebViewSample.as_view(), name="webview-sample"),
]
