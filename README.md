# FlowerShop

Сайт продажи цветов с уведомлением о покупке менеджеру(курьеру)

## Установка

Python 3.10 должен быть уже установлен. Далее используйте `pip`(or `pip3`, если имеется конфликт с Python2)
для установки зависомостей:

```commandline
https://github.com/Weffy61/FlowerShop.git
```

## Установка зависимостей

Переход в директорию с исполняемым файлом

```commandline
cd FlowerShop
```

Установка
```commandline
pip install -r requirements.txt
```

## Создание и настройка .env

Создайте в корне папки `FlowerShop` файл `.env`. Откройте его для редактирования любым текстовым редактором
и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.
Доступны следующие переменные:
 - SECRET_KEY - секретный ключ проекта. Например: `erofheronoirenfoernfx49389f43xf3984xf9384`.
 - TELEGRAM_BOT_API - для уведомлений о покупке в телеграм. Создайте бота в [botfather](https://t.me/BotFather).
 - TG_GROUP_ID - группа в телеграмм для получения заказов. Для того что бы узнать айди группы, нужно добавить [бота](https://t.me/myidbot), и добавить его администратором группы, далее написать /getgroupid.
 - YOOKASSA_SECRET_KEY - ЮKassa секретный ключ. [Что такое YOOKASSA_SECRET_KEY](https://yookassa.ru/docs/support/merchant/payouts/secret-key/).
 - YOOKASSA_SHOP_ID - идентификатор магазина в ЮKassa. [Что такое YOOKASSA_SHOP_ID](https://yookassa.ru/docs/support/merchant/payments/settings).
 - ALLOWED_HOSTS - см [документацию Django](https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts).
 - DEBUG - дебаг-режим. Поставьте True, чтобы увидеть отладочную информацию в случае ошибки.
[Подробнее про DEBUG](https://docs.djangoproject.com/en/4.2/ref/settings/#debug). По умолчанию это  `True`
 - MEDIA_URL - по умолчанию это `'/media/'`. [Что такое MEDIA_URL](https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-MEDIA_URL).
 - STATIC_URL - по умолчанию это `'/static/'`.  [Что такое STATIC_URL](https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-STATIC_URL).


## Подготовка к запуску

1. Переходим, в директорию с `manage.py`, если еще не в ней.

2. Создаем миграции

```commandline
python manage.py makemigrations
```

3. Применяем миграции

```commandline
python manage.py migrate
```

4. Создаём суперпользователя

```commandline
python manage.py createsuperuser
```

## Запуск

```commandline
python manage.py runserver
```

Перейдите по адресу http://127.0.0.1:8000/admin/ и введите данные для авторизации, которые вы указали ранее.
Сам сайт будет запущен по адресу http://127.0.0.1:8000. Для корректной работы создайте Категорию `Без повода`. Создайте
бюджет с уровнем `Не имеет значения`.




