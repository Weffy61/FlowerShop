import textwrap
import uuid

from django.conf import settings
from telebot import TeleBot

from yookassa import Configuration
from yookassa import Payment

from FlowerApp.models import Courier, Order


def create_payment_order(amount, order_num,):
    Configuration.account_id = settings.YOOKASSA_SHOP_ID
    Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

    idempotence_key = str(uuid.uuid4())
    payment = Payment.create({
        "amount": {
          "value": f"{amount}",
          "currency": "RUB"
        },
        "payment_method_data": {
          "type": "bank_card"
        },
        "confirmation": {
          "type": "redirect",
          "return_url": f"http://127.0.0.1:8000/order_confirmation/?&order={order_num}"
        },
        "description": f"Заказ №{order_num}"
    }, idempotence_key)

    confirmation = payment.confirmation.confirmation_url
    return confirmation


def send_message_to_courier_bot(order_id):
    bot = TeleBot(settings.TELEGRAM_BOT_API, threaded=False)
    courier = Courier.objects.filter(status='free').order_by('?').first()
    order = Order.objects.get(pk=order_id)
    order_client_name = order.client_name
    order_phone = order.phone_number
    order_address = order.delivery_address
    bouquet = order.bouquet.name
    delivery_time = order.delivery_time

    message = textwrap.dedent(f'''
        Оплачен новый заказ

        Информация о заказе:
        Заказ №{order_id},
        Заказан букет: {bouquet}
        Информация о клиенте:
        Имя: {order_client_name},
        Телефон: {order_phone},
        Адрес: {order_address},
        Время доставки: {delivery_time}
        ''')
    bot.send_message(courier.tg_id, text=message)
    bot.send_message(settings.TG_GROUP_ID, text=message)
    courier.status = 'busy'
    courier.order = order
    courier.save()
