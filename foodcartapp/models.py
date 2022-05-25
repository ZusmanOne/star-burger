from django.db import models
from django.db.models import Sum, F
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from functools import reduce
import copy


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class OrderQuerySet(models.QuerySet):
    def get_order_price(self):
        return self.annotate(total_price=Sum(F('order_items__price')))

    def get_restaurant(self):
        product_restaurant_menu = RestaurantMenuItem.objects.select_related('product')
        for order in self:
            serialized_restaurants = []
            for order_product in order.order_items.values('product'):
                serialized_restaurants.append([rest_item.restaurant for rest_item in product_restaurant_menu
                                               if order_product['product'] == rest_item.product.pk])
            cooking_restaurant = reduce(set.intersection, map(set, serialized_restaurants))
            order.cooking_restaurant = copy.deepcopy(cooking_restaurant)
        return self


class Order(models.Model):
    ORDER_STATUS = [
        ('UNPROCESSED', 'Не обработан'),
        ('PROCESSED', 'Готовится'),
        ('DONE', 'Выполнен')
    ]

    PAYMENT_METHOD = [
        ('CASH', 'Наличные'),
        ('ONLINE', 'Онлайн')
    ]

    firstname = models.CharField(max_length=100, verbose_name='Имя')
    lastname = models.CharField(max_length=100,  verbose_name='Фамилия')
    phonenumber = PhoneNumberField(verbose_name='Номер телефона', db_index=True)
    address = models.CharField(max_length=200, verbose_name='Адрес')
    comment = models.TextField(verbose_name='Комментарий', blank=True)
    registered_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')
    called_at = models.DateTimeField(db_index=True, verbose_name='Дата Звонка', null=True, blank=True)
    delivery_at = models.DateTimeField(db_index=True, verbose_name='Дата Доставки', null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS,
        db_index=True,
        verbose_name='Статус Заказа',
        default='UNPROCESSED')
    payment_method = models.CharField(
        max_length=20,
        db_index=True,
        choices=PAYMENT_METHOD,
        verbose_name='Способ оплаты')
    cooked_restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='restaurant_orders',
        verbose_name='Готовящий ресторан')

    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"{self.firstname} {self.lastname}, {self.address}"


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product,
        related_name='product_orders',
        on_delete=models.CASCADE,
        verbose_name='Товар')
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name='Заказ')
    quantity = models.IntegerField(
        default=1,
        db_index=True,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        verbose_name='Количество')
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        db_index=True,
        verbose_name='Цена заказа'
    )

    class Meta:
        verbose_name = 'Заказанный товар'
        verbose_name_plural = 'Заказанные товары'

    def __str__(self):
        return f'{self.product}'
