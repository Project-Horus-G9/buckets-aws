import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_email(corpo):

    receiver_email = 'marco.magalhaes@sptech.school'
    subject = 'Alerta de temperatura'
    body = corpo


    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject


    message.attach(MIMEText(body, 'plain'))


    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, smtp_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Enviado")

        server.quit()
    except Exception as e:
        print(f"Houve um erro: {e}")
    finally:
        print("-------------")



