from django.core.mail import send_mail
from django.conf import settings
from threading import Thread


class send_forgot_link(Thread):
    def __init__(self, email, tok, user):
        self.email = email
        self.tok = tok
        Thread.__init__(self)
    def run(self):
        try:
            otp = f"{settings.BASE_URL}{self.user}-reset/{self.tok}/"
            subject = "Link to change password"
            message = f"Click the link to reset your account password\n {otp}"
            email_from = settings.EMAIL_HOST_USER
            print("Email send started")
            send_mail(subject , message ,email_from ,[self.email])
            print("Email send finished")
        except Exception as e:
                print(e)


class send_password_via_mail(Thread):
    def __init__(self, email, password):
        self.email = email
        self.password = password
        Thread.__init__(self)
    def run(self):
        try:
            subject = "Your Login Credentials"
            message = f"Here are your Login Credentials\n Email: {self.email}\n Password: {self.password}"
            email_from = settings.EMAIL_HOST_USER
            print("Email send started")
            send_mail(subject , message ,email_from ,[self.email])
            print("Email send finished")
        except Exception as e:
            print(e)