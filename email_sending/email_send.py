
import asyncio
import smtplib
from email.headerregistry import Address
from email.message import EmailMessage

from aiogram.dispatcher import FSMContext
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from states import Test
from data.config import CONFIG
from smtplibaio import SMTP, SMTP_SSL


# данные почтового сервиса
async def send_email(data: dict):


    user = CONFIG["gmail"]["mail_post"]
    passwd = CONFIG["gmail"]["password"]
    server = "smtp.yandex.ru"
    port = 587
    # тема письма
    subject = "Пользователь прошел тест"
    # кому
    to = CONFIG["gmail"]["mail_get"]

    msg = MIMEMultipart()
    msg["From"] = user
    msg["To"] = to
    msg["Subject"] = subject
    if str(data['currency']) == 'rub':
        msg.attach(MIMEText(str(data['apply'])  + ' ' + str(data['cryptocurrencytotal']) + ' ' + str(data["cryptocurrency"]) + ' ' + str('BYN') + ' ' + str(data["currency_price"]), "plain"))
    else:
        msg.attach(MIMEText(
            str(data['apply']) + ' ' + str(data['cryptocurrencytotal']) + ' ' + str(data["cryptocurrency"]) + ' ' + str(
                data['currency']) + ' ' + str(data["currency_price"]), "plain"))
    smtp = smtplib.SMTP(server, port)
    try:
        # подключаемся к почтовому сервису

        smtp.starttls()
        smtp.ehlo()
        # логинимся на почтовом сервере
        smtp.login(msg["From"], passwd)
        # пробуем послать письмо
        smtp.sendmail(msg["From"], msg["To"], msg.as_string())
    except smtplib.SMTPException as err:
        print('Что - то пошло не так...')
        raise err
    finally:
        print('Письмо успешно отправлено')
        smtp.quit()