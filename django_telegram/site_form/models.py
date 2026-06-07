from django.db import models


# Create your models here.

class SiteModel(models.Model):
    name = models.CharField('Имя', max_length=100)
    surname = models.CharField('Фамилия', max_length=100)
    text = models.TextField('Текст')
    date = models.DateTimeField('Дата')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Форма'
        verbose_name_plural = 'Формы'
