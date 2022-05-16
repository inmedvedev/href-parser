from django.db import models


class DomainInfo(models.Model):
    base_url = models.URLField(
        'ссылка поиска',
        null=True,
        blank=True
    )
    url = models.URLField(
        'найденная ссылка'
    )
    domain = models.CharField(
        'домен',
        max_length=500
    )
    create_date = models.DateTimeField()
    update_date = models.DateTimeField()
    country = models.CharField(
        'страна',
        max_length=100,
        null=True
    )
    is_dead = models.BooleanField(
        'домен мертв?'
    )


class Address(models.Model):
    url = models.ForeignKey(
        DomainInfo,
        on_delete=models.CASCADE
    )
    ip = models.GenericIPAddressField(
        null=True,
        blank=True
    )


class NameServer(models.Model):
    url = models.ForeignKey(
        DomainInfo,
        on_delete=models.CASCADE
    )
    name = models.CharField(
        'имя сервера',
        max_length=500
    )


class MailExchange(models.Model):
    url = models.ForeignKey(
        DomainInfo,
        on_delete=models.CASCADE
    )
    exchange = models.CharField(
        'почтовый шлюз',
        max_length=500,
        null=True
    )
    priority = models.SmallIntegerField(default=None)


class TxtRecord(models.Model):
    url = models.ForeignKey(
        DomainInfo,
        on_delete=models.CASCADE
    )
    txtrecord = models.CharField(
        'текстовая информация о домене',
        max_length=500,
        null=True
    )
