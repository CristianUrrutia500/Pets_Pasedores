# reset/urls.py

from django.urls import path
from .views import CustomPasswordResetView, CustomPasswordResetCompleteView
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView

urlpatterns = [
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='reset/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='reset/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
