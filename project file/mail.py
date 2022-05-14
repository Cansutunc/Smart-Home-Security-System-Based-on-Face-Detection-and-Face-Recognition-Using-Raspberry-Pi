import smtplib
import imghdr
from email.message import EmailMessage
import datetime

def send_mail(name):

    Sender_Email = "myraspberrypiprojects@gmail.com"
    Reciever_Email = "..."#your mail acoount
    Password = "Raspberrypi123"

    newMessage = EmailMessage()                         
    newMessage['Subject'] = "Raspberry Pi Facial Recognition System" 
    newMessage['From'] = Sender_Email                   
    newMessage['To'] = Reciever_Email                   
    newMessage.set_content(f"Name:{name}\nTime:{datetime.datetime.now()}")
    
    with open('photo.jpg', 'rb') as f: #embed image
        image_data = f.read()
        image_type = imghdr.what(f.name)
        image_name = f.name

    newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        
        smtp.login(Sender_Email, Password)              
        smtp.send_message(newMessage)

    print("Mail sended to " + Reciever_Email)

