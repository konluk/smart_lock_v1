import smtplib
from email.message import EmailMessage

#\n - enter
def sendEmail(email, subject, message):

    msg = EmailMessage()
    msg.set_content(message)

    msg['Subject'] = subject
    msg['From'] = "inteligentny.elektricky.vratnik@gmail.com"
    msg['To'] = email

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login("inteligentny.elektricky.vratnik@gmail.com", "Vratnik123")
    server.send_message(msg)
    server.quit()