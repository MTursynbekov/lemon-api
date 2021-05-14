import mptt
from datetime import date
from django.contrib.postgres.fields import IntegerRangeField
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from utils.constants import PRODUCT_TYPE, WOMEN_PRODUCT


class Category(MPTTModel):
    name = models.CharField(max_length=50,
                            verbose_name="Название категории")
    parent = TreeForeignKey('self',
                            on_delete=models.DO_NOTHING,
                            null=True, blank=True,
                            related_name='sub_categories',
                            verbose_name="Родитель категории")

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ('tree_id', 'level')

    def __str__(self):
        return f'{self.name}'

    def __unicode__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название города")

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"

    def __str__(self):
        return f'{self.name}'


class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название бренда")

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"

    def __str__(self):
        return f'{self.name}'


class Store(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название магазина")
    address = models.TextField(verbose_name="Адрес магазина")
    brand = models.ForeignKey(Brand,
                              on_delete=models.CASCADE,
                              related_name="stores",
                              verbose_name="Бренд",
                              blank=True,
                              null=True)

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"

    def __str__(self):
        return f'{self.name}'


class Promotion(models.Model):
    src = models.ImageField(upload_to="images/promotions")
    duration = models.DurationField(verbose_name="Срок акции")
    brand = models.ForeignKey(Brand,
                              on_delete=models.CASCADE,
                              related_name="promotions",
                              verbose_name="Бренд",
                              blank=True,
                              null=True)

    class Meta:
        verbose_name = "Акция"
        verbose_name_plural = "Акции"

    def __str__(self):
        return f'Акция brand: {self.brand}'


class Product(models.Model):
    name = models.CharField(max_length=300, verbose_name="Название продукта")
    price = models.FloatField(verbose_name="Цена")
    discount = models.PositiveSmallIntegerField(default=0, verbose_name='Скидка')
    in_stock = models.BooleanField(default=False, verbose_name='Есть в наличии?')
    in_top = models.BooleanField(default=False, verbose_name='В топе?')
    short_description = models.CharField(blank=True, null=True, max_length=100, verbose_name="Краткое описание")
    long_description = models.TextField(blank=True, null=True, verbose_name="Описание")
    publication_date = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    discount_ends_date = models.DateField(default=date.today, verbose_name="Время окончания скидки")
    type = models.CharField(choices=PRODUCT_TYPE,
                            default=WOMEN_PRODUCT,
                            verbose_name="Тип продукта",
                            max_length=1)
    category = TreeForeignKey(Category,
                              on_delete=models.CASCADE,
                              related_name="products",
                              verbose_name="Категория",
                              blank=True,
                              null=True)
    city = models.ForeignKey(City,
                             on_delete=models.CASCADE,
                             related_name="products",
                             verbose_name="Город",
                             blank=True,
                             null=True)
    brand = models.ForeignKey(Brand,
                              on_delete=models.CASCADE,
                              related_name="products",
                              verbose_name="Бренд продукта",
                              blank=True,
                              null=True)
    stores = models.ManyToManyField(Store,
                                    related_name="products",
                                    verbose_name="Магазины")

    class Meta:
        ordering = ['-publication_date']
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f'{self.name}'

    @property
    def price_with_discount(self):
        return self.price * (1 - self.discount // 100)


class ProductSpecification(models.Model):
    key = models.CharField(max_length=50, verbose_name='Ключ')
    value = models.CharField(max_length=50, verbose_name='Значение')
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                verbose_name='Продукт',
                                related_name='specifications',
                                blank=True,
                                null=True)

    class Meta:
        verbose_name = 'Характеристика продукта'
        verbose_name_plural = 'Характеристики продукта'


class ProductImage(models.Model):
    src = models.ImageField(upload_to='images/product')
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name="images",
                                verbose_name="Продукт",
                                blank=True,
                                null=True)

    class Meta:
        verbose_name = "Картинка продукта"
        verbose_name_plural = "Картинки продукта"
