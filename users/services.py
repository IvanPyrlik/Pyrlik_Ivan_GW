import os
import prosto_sms
import stripe
from django.shortcuts import redirect

from config.settings import STRIPE_API_KEY
from users.models import User
import random

stripe.api_key = STRIPE_API_KEY


def create_sessions():
    """
    Создаем сессию на оплату в страйпе.
    """
    amount = 500   # Сумма платежа.
    product = stripe.Product.create(name='Подписка')  # Создаем подписку.
    price = stripe.Price.create(
        currency="usd",
        unit_amount=amount,
        product=f'{product.id}',
    )  # Создаем цену.

    session = stripe.checkout.Session.create(
        success_url='https://example.com/success',
        line_items=[{"price": price.id, "quantity": 1}],
        mode="payment",
    )  # Создаем сессию.
    return session


def session_check(session_id):
    """
    Проверка оплаты.
    """
    session = stripe.checkout.Session.retrieve(
        f"{session_id}",
    )

    pay_status = session['pay_status']
    print('session=', session)
    return pay_status


def get_key():
    """
    Генерация ключа.
    """
    key = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    return key


def send_key(phone, key):
    """
    Отправка СМС.
    """
    api = prosto_sms.API(
        email=os.getenv('EMAIL_SMS'),
        password=os.getenv('PASSWORD_SMS')
    )
    api.methods.push_message(text=f'Код для регистрации: {key}', phone=f'{phone}')

    return redirect('users:confirm_phone')


def activ_sub():
    """
    Активация подписки.
    """
    sub_not = User.objects.filter(
        pay_id__isnull=False,
        activ_subscription=False
    )

    for user in sub_not:
        if session_check(user.pay_id) == "paid":
            user.activ_subscription = True
            user.pay_id = None
            user.save()


def cleaner_key():
    """
    Очистка ключей.
    """
    users_with_key = User.objects.filter(
        key__isnull=False,
    )

    for user in users_with_key:
        user.key = None
        user.save()
