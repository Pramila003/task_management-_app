from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType 
from pydantic import EmailStr, BaseModel
from typing import List



conf = ConnectionConfig(
    MAIL_USERNAME= "pramila.yamgar007@gmail.com",
    MAIL_PASSWORD="lfoi xghb voxg ufde",
    MAIL_FROM="pramila.yamgar007@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="pramila fastapi ",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True

)

async def send_mail(emails:List[str]):
    html = """<p>Hi this test mail, thanks for using Fastapi-mail</p> """

    message = MessageSchema(
        subject="Registration Confirmation",
        recipients=emails,
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    print ({"message":"email has been sent"})