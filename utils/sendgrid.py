from sendgrid.helpers.mail import Mail
import sendgrid
import os


def sendgrid_send_mail(subject, body, _from, to):
    message = Mail(
        from_email=os.environ.get('FROM_EMAIL'),
        to_emails=to,
        subject=subject,
        html_content=body,
     )

    try:
        sg = sendgrid.SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        sg.client.mail.send.post(request_body=message.get())
        return True
    except Exception as e:
        return e
