from django.db import models


class Product(models.Model):
    name = models.CharField(
        max_length=1000,
        verbose_name='Название товара'
    )
    price = models.IntegerField(
        verbose_name='Цена'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    image_url = models.URLField(
        verbose_name='Ссылка на изображение'
    )
    discount = models.CharField(
        verbose_name='Скидка',
        max_length=100,
        null=True,
        blank=True
    )
    url = models.URLField(
        verbose_name='Ссылка на товар'
    )
