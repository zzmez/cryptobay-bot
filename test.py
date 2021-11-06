import json
import smtplib

def send_mail_sold():
    gmail_user = 'miezuaa@gmail.com'

    with open("tools/zzsecrets.json") as f:
        data = json.load(f)
        gmail_password = data['GMAIL_APP_PASS']

    sent_from = gmail_user
    to = [gmail_user]
    subject = 'SOLD boat111111'
    body = 'Account a SOLD a boat'

    email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)
    print(email_text)
    
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print('Email sent!')
    except:
        print('Something went wrong...')

send_mail_sold()
