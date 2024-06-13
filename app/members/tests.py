from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import Member


class LoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user = Member.objects.create_user(
            member_email="test@example.com", 
            display_name="Test User", 
            member_password="password123"
        )

    def test_login_page(self):
        response = self.client.get(reverse("member-login"))
        self.assertEqual(response.status_code, 200)

    def test_login_form(self):
        response = self.client.post(
            reverse("member-login"),
            {"member_email": self.test_user.member_email, "member_password": "password123"},
        )
        self.assertEqual(response.status_code, 302)  # 로그인 성공 후 리디렉션을 가정
