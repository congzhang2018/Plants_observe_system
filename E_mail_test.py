#!/usr/bin/python

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

fromaddr = "congzworking@gmail.com"
toaddr = "zc188113236@gmail.com"
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Test_email!!"
 
body = "This is a test email!!"
msg.attach(MIMEText(body, 'plain'))
 
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "zc188113236")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
