# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-06-11 14:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoices',
            name='payment_method',
            field=models.CharField(blank=True, default='CREDITCARD', max_length=100),
        ),
    ]