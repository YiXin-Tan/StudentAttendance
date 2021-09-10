import os
import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
# from email.utils import formatdate
from email import encoders

def send_mail(start_time, csv_filepath):
    class_datetime = start_time.strftime('%Y-%m-%d %H:%M')

    sender_email = 'cacticatocat@gmail.com'
    sender_pwd = os.environ.get('SMTP_SENDER_PWD')

    # Insert email recipient below:
    receiver_email = 'test@example.com'

    body = f'<h5>{class_datetime} Attendance</h5>' \
           f'<p>Innovative Solution developed by:\n2021 CO011A GroupC</p><hr>'
    filename = f'{class_datetime} Attendance List.csv'

    message = MIMEMultipart()
    message['Subject'] = f'CO011A Attendance {class_datetime}'
    message['From'] = sender_email
    message['To'] = receiver_email

    part1 = MIMEText(body, _subtype='html')
    message.attach(part1)

    with open(csv_filepath, 'rb') as attachment:
        part2 = MIMEApplication(attachment.read())
    encoders.encode_base64(part2)
    part2.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )
    message.attach(part2)

    smtp_server = 'smtp.gmail.com'
    port = 465
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(user=sender_email, password=sender_pwd)
        server.sendmail(from_addr=sender_email, to_addrs=receiver_email, msg=message.as_string())
