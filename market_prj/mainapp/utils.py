# import requests
# import logging
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_email_message(subject, context, recipient):
    # connection = get_connection()
    # connection.open()
    from_email = settings.EMAIL_HOST_USER
    html_content = render_to_string("mainapp/notification.html", context)
    msg = EmailMultiAlternatives(subject, 'текст сообщения из функции', from_email, [recipient])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    # connection.close()


# def send_sms_message(transaction, phone_number):
#     name = transaction["car"] or transaction["card"] or ""
#     text_message = (
#         f"{name}: карта {transaction['card_volume']} ДУТ {transaction['car_volume']} "
#         f"разница {transaction['diff_volume']} дата {transaction['datetime']}"
#     )
#     send_sms(phones=["+7" + phone_number], text=text_message)
#
#
# def send_sms(phones, text):
#     messages = [
#         {
#             "recipient": str(phone),
#             "recipientType": "recipient",
#             "id": "1",
#             "source": "SPD_Server",
#             "timeout": 3600,
#             "shortenUrl": True,
#             "text": text,
#         }
#         for phone in phones
#     ]
#     payload = {"messages": messages, "validate": False, "transliterate": False}
#     headers = {
#         "Content-Type": "application/json",
#         "X-Token": settings.SMS_TOKEN,
#     }
#     try:
#         r = requests.post(
#             settings.SMS_URL, json=payload, headers=headers, timeout=5, verify=False
#         )
#         if r.status_code != requests.codes.ok:
#             logger.error(f"Failed to send sms: {r.status_code}")
#             return
#         response = r.json()
#         if not response["success"]:
#             logger.error(response.get("error"))
#
#     except (IOError, TimeoutError) as err:
#         logger.error(err)
