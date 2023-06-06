from django.core.mail import send_mail, EmailMessage, send_mass_mail
from django.conf import settings


def send_email(to):
    # send_mail("test", "my message ", settings.EMAIL_HOST_USER, [to, ])
    msg = EmailMessage("my first email", '<p>This is an <strong>important</strong> message.</p>', settings.EMAIL_HOST_USER, [to])
    msg.content_subtype = "html"  # Main content is now text/html


def send_mass_email():
    message1 = ('Subject here', 'Here is the message', settings.EMAIL_HOST_USER, ["vitragtest@mailinator.com", "vitragpatel2408@gmail.com"])
    message2 = ('Another Subject', 'Here is another message', settings.EMAIL_HOST_USER, ['vitragtest@mailinator.com'])
    send_mass_mail((message1, message2), fail_silently=False)

