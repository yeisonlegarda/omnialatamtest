from django.core.mail import EmailMessage
from django.conf import settings
from principal.models import User

MAIL_SUBJECT = "{order} order {typenot} notification"
MAIL_MESSAGE = "The {order} was {typenot} on {date} "


async def send_email(request):
    try:
        user = request.user
        order = request.data.get('order')

        typenot = 'sent'
        date = request.data.get('sent_date')
        if request.data.get('received_date'):
            typenot = 'received'
            date = request.data.get('received_date')

        subject = MAIL_SUBJECT.format(order=order, typenot=typenot)
        message = MAIL_MESSAGE.format(order=order,typenot=typenot, date=date)
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=[user.email]
        )
        email.send()
        response = {"Success sending mail"}
    except Exception as e:
        response = {"Error sending mail"}
    return response
