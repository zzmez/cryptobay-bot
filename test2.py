import json
import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



gmail_user = 'miezuaa@gmail.com'

with open("tools/zzsecrets.json") as f:
    data = json.load(f)
    gmail_password = data['GMAIL_APP_PASS']

sent_from = gmail_user
to = [gmail_user]
msg = MIMEMultipart()
msg['subject'] = 'sold boat3'
msg['From'] = sent_from

df_test = pd.read_csv("db/accounts/account_status.csv")

html = f"""
<html>
  <head></head>
  <body>
    {df_test.to_html(index=False)}
  </body>
</html>
""".format()

part1 = MIMEText(html, 'html')
msg.attach(part1)

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(msg['From'], to, msg.as_string())
    server.close()

    print('Email sent!')
except:
    print('Something went wrong...')