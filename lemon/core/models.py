import mptt
from datetime import date
from django.contrib.postgres.fields import IntegerRangeField
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from utils.constants import CATEGORY_TYPES, CATEGORY_TYPE_CLOTHES, PRODUCT_TYPE, WOMEN_PRODUCT


class Category(MPTTModel):
    name = models.CharField(max_length=50,
                            verbose_name="Название категории")
    parent = TreeForeignKey('self',
                            on_delete=models.CASCADE,
                            null=True, blank=True,
                            related_name='children',
                            verbose_name="Родитель категории")
    type = models.SmallIntegerField(choices=CATEGORY_TYPES,
                                    default=CATEGORY_TYPE_CLOTHES,
                                    verbose_name="Тип категории")

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


mptt.register(Category, order_insertion_by=['name'])


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
    src = models.ImageField(upload_to="images/promotion")
    duration = models.DurationField(verbose_name="Срок акции")
    brand = models.ForeignKey(Brand,
                              on_delete=models.CASCADE,
                              related_name="special_offers",
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
    in_stock = models.BooleanField(default=False, verbose_name='Есть в наличии?')
    short_description = models.CharField(max_length=100, verbose_name="Краткое описание")
    description = models.TextField(verbose_name="Описание", default="")
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

    def __str__(self):
        return f'Картинки product: {self.product}'


class Clothes(Product):
    size = IntegerRangeField(verbose_name="Размер")
    euro_size = models.CharField(max_length=10,
                                 blank=True,
                                 null=True,
                                 verbose_name="Размер, европейский стандарт")

    class Meta:
        verbose_name = "Одежда"


class Shoes(Product):
    size = IntegerRangeField(verbose_name="Размер")

    class Meta:
        verbose_name = "Обувь"


class Accessories(Product):
    class Meta:
        verbose_name = "Аксессуар"
        verbose_name_plural = "Аксессуары"
