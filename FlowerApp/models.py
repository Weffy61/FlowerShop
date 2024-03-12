from django.core.validators import MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Store(models.Model):
    address = models.CharField(verbose_name='Адрес', max_length=200)
    phone_number = PhoneNumberField(verbose_name='Телефон')

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self):
        return f'Магазин {self.pk}'


class Bouquet(models.Model):
    name = models.CharField(verbose_name='Название', max_length=200)
    price = models.DecimalField(verbose_name='Цена', max_digits=8, decimal_places=2, validators=[MinValueValidator(1)])
    image = models.ImageField(verbose_name='Изображение', upload_to='images/')
    compound = models.TextField(verbose_name='Состав')
    size_height = models.SmallIntegerField(verbose_name='Высота букета')
    size_width = models.SmallIntegerField(verbose_name='Ширина букета')
    category = models.ManyToManyField(
        'BouquetCategory',
        verbose_name='Категория букета',
        related_name='bouquets'
    )

    class Meta:
        verbose_name = 'Букет'
        verbose_name_plural = 'Букеты'

    def __str__(self):
        return f'Букет {self.name}'


class BouquetCategory(models.Model):
    name = models.CharField(verbose_name='Наименование категории', max_length=200)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'Категория {self.name}'


class Order(models.Model):
    bouquet = models.ForeignKey(Bouquet, on_delete=models.CASCADE, verbose_name='Букет', related_name='orders')
    client_name = models.CharField(verbose_name='Имя клиента', max_length=200)
    phone_number = PhoneNumberField(verbose_name='Телефон')
    delivery_address = models.TextField(verbose_name='Адрес доставки')
    payment_status = models.BooleanField(verbose_name='Оплачен', default=False)
    DELIVERY_TIME_CHOICES = (
        ('as_soon_as_possible', 'Как можно скорее'),
        ('10_to_12', 'С 10:00 до 12:00'),
        ('12_to_14', 'С 12:00 до 14:00'),
        ('14_to_16', 'С 14:00 до 16:00'),
        ('16_to_18', 'С 16:00 до 18:00'),
        ('18_to_20', 'С 18:00 до 20:00'),
    )
    delivery_time = models.CharField(max_length=50, choices=DELIVERY_TIME_CHOICES)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'ID заказа {self.id}'


class Courier(models.Model):
    tg_id = models.BigIntegerField(verbose_name='TG id курьера')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ', related_name='couriers')
    STATUS_CHOICES = (
        ('free', 'Free'),
        ('busy', 'Busy')
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    class Meta:
        verbose_name = 'Курьер'
        verbose_name_plural = 'Курьеры'

    def __str__(self):
        return f'ID курьера {self.tg_id}'


class ConsultationRequest(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=255)
    phone_number = PhoneNumberField(verbose_name='Телефон')
    date = models.DateField(verbose_name='Дата', auto_now_add=True)

    class Meta:
        verbose_name = 'Консультация'
        verbose_name_plural = 'Консультации'

    def __str__(self):
        return self.name
    