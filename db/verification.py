import configparser
import random
import smtplib
from email.mime.text import MIMEText


def send_email(email):
    configload = configparser.RawConfigParser()
    configload.read('../server.properties')
    sender = configload.get('verification', 'email')
    password = configload.get('verification', 'password')

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(sender, password)
        msg = MIMEText('Your verification code is: ' + str(random.randint(100000, 999999)))
        msg["Subject"] = "Verification code"
        server.sendmail(sender, email, msg.as_string())

        return "The message was sent successfully!"
    except Exception as _ex:
        return f"{_ex}\nCheck your login or password please!"


