from django.test import TestCase

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from reset.views import (
    CustomPasswordResetView,
    CustomPasswordResetCompleteView
)
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView

class TestUrls(SimpleTestCase):
    def test_password_reset_url_resolves(self):
        url = reverse('password_reset')
        self.assertEquals(resolve(url).func.view_class, CustomPasswordResetView)

    def test_password_reset_done_url_resolves(self):
        url = reverse('password_reset_done')
        self.assertEquals(resolve(url).func.view_class, PasswordResetDoneView)

    def test_password_reset_confirm_url_resolves(self):
        url = reverse('password_reset_confirm', args=['uidb64', 'token'])
        self.assertEquals(resolve(url).func.view_class, PasswordResetConfirmView)

    def test_password_reset_complete_url_resolves(self):
        url = reverse('password_reset_complete')
        self.assertEquals(resolve(url).func.view_class, CustomPasswordResetCompleteView)

