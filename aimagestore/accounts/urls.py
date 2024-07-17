from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('email/', views.email_view, name='email'),
    path('new-password/', views.change_password_view, name='new-password'),
    path('code-verification/', views.code_verification_view, name='code-verification'),
    path('resend-otp/', views.resend_otp, name='resend-otp'),
    path('logout/', views.logout_view, name='logout'),
]
