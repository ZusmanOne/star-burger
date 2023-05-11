from django.db import models


class Banner(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100,unique=True)
    image = models.ImageField(verbose_name='Изображение баннера',upload_to='banner_image/%Y/%m')

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'

    def __str__(self):
        return self.title

# Create your models here.
